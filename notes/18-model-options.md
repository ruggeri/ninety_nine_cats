# Model Options

* `abstract`: this is used to not instantiate a table for the model
  class. Instead, this is supposed to be used as a base class. It allows
  you to write your own `TimeStampedModel` class.
* `db_table`: like it sounds. You set the db table name.
* `managed`: if you set this to false, then Django won't make migrations
  to make/modify this table. Useful for pre-existing tables.
* `ordering`: You can set a column to apply for default ordering. I
  personally wouldn't use this.
* `indexes`: covered elsewhere.
* `constraints`: covered elsewhere.
