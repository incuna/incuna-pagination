# `incuna-pagination` [![Build Status](https://magnum.travis-ci.com/incuna/incuna-pagination.svg?token=9QKsFUYHUxekS7Q4cLHs&branch=master)](https://travis-ci.org/incuna/incuna-pagination)

Utilities for paginated views.
- Provides a template tag that allows you to generate URLs with modified querystrings.
- Provides an include template that displays a nice pagination menu.

## Installation

`incuna-pagination` is on PyPI, so you can install it with `pip install incuna-pagination`.  Add `pagination` to your `INSTALLED_APPS`.

## Usage

`{% include "includes/_pagination.html" %}` will add the pagination display to a Django template.
