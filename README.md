# `incuna-groups` [![Build Status](https://magnum.travis-ci.com/incuna/incuna-groups.svg?token=9QKsFUYHUxekS7Q4cLHs&branch=master)](https://travis-ci.org/incuna/incuna-groups)

An extensible Django app that provides forum functionality.
- Administrators can create discussion groups.
- Users can create discussions on groups, and comment on those discussions.
- Users can also subscribe to groups and/or discussions to receive notifications from them, and post responses by replying to the notification emails. 

## Installation

`incuna-groups` is on PyPI, so you can install it with `pip install incuna-groups`.  Add `groups` to your `INSTALLED_APPS`.

This project contains migrations, so run `python manage.py migrate` before using it.

## Usage

`incuna-groups` is self-contained - it provides models, views, and templates.  At the moment, it doesn't provide styling or a REST API.

Some straightforward customisation is exposed through the `AppConfig` (which by default is `groups.apps.GroupsConfig`) and the templates can all be overridden easily.

Each page template has a `base` version that the page template itself directly `extends`, meaning you can replace the page template but still make use of all of the blocks and other HTML in the original.  For instance, `discussion_thread.html` does nothing other than extend `discussion_thread_base.html`.  You can override `discussion_thread.html`, extend `discussion_thread_base.html` in the same way, and change the content of, say, a single block, rather than having to copy and paste the entirety of the discussion thread template in and modify from there. 

### Models

There are three main models that everything revolves around, one of which is polymorphic for easy extension.

- `Group`: A group that contains any number of discussions, like a forum board.  Created in the Django admin, and holds discussion threads added by users.  A group can be denoted as private, in which case a user has to request to join it before they can read or post any comments.  A group can also have moderators who have the ability to delete or edit other users' comments.  Users can subscribe to a group, which will send them notifications for any discussions created on the group or comments posted to discussions in the group.
- `Discussion`: A single discussion thread, with at least one comment on it (the initial one).  Created by a user.  Users can comment on and subscribe to discussions.  If a user is already subscribed to a discussion's parent group, they can "unsubscribe" from the discussion, which will (internally) cause the discussion to be 'ignored' for that user, and they won't get any notifications for it.
- `BaseComment`: A `django-polymorphic` base class for `Comment`s.  Doesn't do anything by itself, but is used for testing and to refer to arbitrary different kinds of comment.  Subclasses of `BaseComment` are picked up by the discussion-related views.  It comes with some subclasses:
  * `TextComment`: A comment with a text body - an entirely ordinary message.
  * `FileComment`: A comment containing an uploaded file.

Each of the three main models also has a custom queryset (which is then used by its manager) with several additional methods.  Most of them allow fetching of recently active items or accessing groups/discussions/comments related to any instance of any of the three.  These querysets and methods can be found in `managers.py`.
  
### Views and admin pages

There are a lot of different views that come together to make the forums work.

- `Group`
  * Created by `admin.GroupAdmin` - in the Django admin
  * Listed by `views.groups.GroupList`
  * Detailed by `views.groups.GroupDetail` - implemented as a `ListView` for `Discussion`s, to display the group's contents.
  * Subscribed to by `views.subscriptions.GroupSubscribe`
- `Discussion`
  * Created by `admin.DiscussionAdmin` - in the Django admin
  * Created by `views.discussions.DiscussionCreate` - this one also creates the `Discussion`'s first comment, currently a `TextComment`.
  * Listed by `views.groups.GroupDetail`
  * Detailed by `views.discussions.DiscussionThread` - implemented as a `CommentPostView` from `views._helpers`, to allow people to reply via the discussion page itself.
  * Subscribed to by `views.subscriptions.DiscussionSubscribe`
- `Comment`
  * Created by `views._helpers.CommentPostView` - a base class that both creates comments and sends email notifications to relevant people.
  * Created by `views.discussions.DiscussionThread` - the discussion thread page provides an inline reply form that submits `TextComment`s.
  * Created by `views.comments.CommentUploadFile` - a separate page for the uploading of `FileComment`s.
  * Created by `views.comments.CommentPostByEmail` - an endpoint suitable for receiving email replies via Mailgun.
  * Listed by `views.discussions.DiscussionThread`
  * Deleted by `views.comments.CommentDelete` - a comment provides a 'delete' button which will archive it and hide its contents from view.

## Notes on features

### `AppConfig`

`incuna-groups` has an `AppConfig`, located in `apps.py`, which allows for easy customisation of some of its behaviour.  The documentation on `AppConfig`s (and their use) is here: https://docs.djangoproject.com/en/1.8/ref/applications/#for-application-users

The `AppConfig` exposes:
- `default_within_days` - a default parameter for the `within_days` methods on some of the model managers, which return items that were posted or posted to within that time period.
- `new_comment_subject` and `new_discussion_subject` - subjects for notification emails.  Each one will be formatted with the `{discussion}` a comment is on or the `{group}` a discussion belongs to, respectively.
- `group_admin_class_path` and `discussion_admin_class_path` - these allow you to override the admin behaviour of `incuna-groups` by slotting in alternate `ModelAdmin` classes.  These may or may not be based on the existing admin classes in `admin.py`.

### Email notifications

Whenever a discussion is created in a group, users subscribed to that group get an email notification.  Whenever a comment is posted to a discussion, users subscribed to that discussion or its parent group also receive email notifications.

The email templates are in `templates/groups/emails`.  Discussion notifications are sent by `views.discussions.DiscussionCreate`; comment notifications are sent by subclasses of `CommentEmailMixin` (`CommentPostView`, `DiscussionThread` and `CommentUploadFile`).

### Email replies

Users can reply to discussions or comments by replying to the notification emails.  Email replies are implemented by an endpoint (`/groups/reply/`, serving up the `CommentPostByEmail` view) that accepts POST requests containing JSON content representing the email.  The library is set up to work with [Mailgun](https://www.mailgun.com/) routes.

The user and discussion are identified by a crafted `Reply-To` header, which contains a reply address of `reply-{uuid}@{domain}`.  The UUID is generated by securely signing a dictionary of the user and discussion PKs, and unpacked by the endpoint when it receives Mailgun's JSON message.  Mailgun provides a `stripped-text` field that removes quotes and signatures from the content of the email, so there's no need for users to reply in a specific way or for us to do any of that processing ourselves.

A rough API description for Mailgun can be [found here](http://blog.mailgun.com/handle-incoming-emails-like-a-pro-mailgun-api-2-0/).  The POST and files data will be in `request.POST` and `request.FILES` respectively.

There are a couple of gotchas:

- The `/groups/reply/` endpoint _has a trailing slash_.  Ensure that this slash is included in any Mailgun route destination otherwise you'll get a stream of HTTP301s.
- If you're using [`incuna_auth.LoginRequiredMiddleware`](https://github.com/incuna/incuna-auth/blob/master/incuna_auth/middleware/login_required.py#L28), make sure to add `/groups/reply/` to `LOGIN_EXEMPT_URLS` to avoid more 301s.
- The `CommentPostByEmail` view has a `@csrf_exempt` decorator on the `dispatch()` method to avoid CSRF-related HTTP403 errors.  If you extend the class, make sure to add the CSRF exemption.

### Overriding admin classes

`Group` and `Discussion` both have custom admin classes, defined in `admin.py`.  Both of these can be easily replaced by way of the `AppConfig` (see above).  The `AppConfig` registers these admin classes for you, so don't call `admin.site.register` yourself.
