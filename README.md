# Vendor service

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/458b1c5dc55641babf4210571595367c)](https://www.codacy.com/gh/TNLinc/Vendor/dashboard?utm_source=github.com&utm_medium=referral&utm_content=TNLinc/Vendor&utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/TNLinc/CV/branch/main/graph/badge.svg?token=FORLTJT0TH)](https://codecov.io/gh/TNLinc/CV)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![CodeFactor](https://www.codefactor.io/repository/github/tnlinc/vendor/badge)](https://www.codefactor.io/repository/github/tnlinc/vendor)

We decided to use FastApi as one of the fastest and useful framework. As ORM we
used a new library called SQL models. It contains sqlalchemy and pydantic model
in one model.

With this service you can:

- get vendor info by id
- get all vendors
- get product info by id
- get all products
- get products by color

This server has API specification (check another Wiki page
called [Vendor API](https://github.com/KochankovID/TonalCreamAssistant/wiki/Vendor-API))
