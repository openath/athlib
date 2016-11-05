"""
This file covers testing validity of JSON schemata, plus the fields in the
schemta themselves.
"""

import json
import jsonschema
from jsonschema.exceptions import SchemaError,ValidationError
from unittest import TestCase, main


def schema_valid(schema_file):
	with open(schema_file) as f:
		schema = json.load(f)

		try:
			jsonschema.Draft3Validator.check_schema(schema)
			jsonschema.Draft4Validator.check_schema(schema)
			return True
		except SchemaError as e:
			print(e)
			return False

	return False

def valid_against_schema(json_file, schema_file):
	with open(json_file) as f:
		json_data = json.load(f)

		with open(schema_file) as f2:
			schema = json.load(f2)

    		try:
    			jsonschema.validate(json_data, schema)
    			return True
    		except ValidationError as e:
    			print(e)
    			return False

	return False


class JsonSchemaValidityTests(TestCase):
    def test_metaschema_valid(self):
        self.assertTrue(schema_valid("json/metaschema.json"))

    def test_athlete_schema_valid(self):
        self.assertTrue(schema_valid("json/athlete.json"))

    def test_combined_performance_schema_valid(self):
        self.assertTrue(schema_valid("json/combined_performance.json"))

    def test_competition_schema_valid(self):
        self.assertTrue(schema_valid("json/competition.json"))

    def test_event_schema_valid(self):
        self.assertTrue(schema_valid("json/event.json"))

    def test_performance_schema_valid(self):
        self.assertTrue(schema_valid("json/performance.json"))

    def test_athlete_valid_against_schema(self):
    	self.assertTrue(valid_against_schema("json/samples/athlete.json", "json/athlete.json"))
    	self.assertTrue(valid_against_schema("json/samples/athlete_minimal.json", "json/athlete.json"))

    def test_athlete_invalid_against_schema(self):
    	self.assertFalse(valid_against_schema("json/samples/athlete_invalid.json", "json/athlete.json"))

    def test_combined_performance_valid_against_schema(self):
    	self.assertTrue(valid_against_schema("json/samples/combined_performance.json", "json/combined_performance.json"))
    	self.assertTrue(valid_against_schema("json/samples/combined_performance_minimal.json", "json/combined_performance.json"))

    def test_combined_performance_invalid_against_schema(self):
    	self.assertFalse(valid_against_schema("json/samples/combined_performance_invalid.json", "json/combined_performance.json"))

    def test_competition_valid_against_schema(self):
    	self.assertTrue(valid_against_schema("json/samples/competition.json", "json/competition.json"))
    	self.assertTrue(valid_against_schema("json/samples/competition_minimal.json", "json/competition.json"))

    def test_competition_invalid_against_schema(self):
    	self.assertFalse(valid_against_schema("json/samples/competition_invalid.json", "json/competition.json"))

    def test_event_valid_against_schema(self):
    	self.assertTrue(valid_against_schema("json/samples/event.json", "json/event.json"))
    	self.assertTrue(valid_against_schema("json/samples/event_minimal.json", "json/event.json"))

    def test_event_invalid_against_schema(self):
    	self.assertFalse(valid_against_schema("json/samples/event_invalid.json", "json/event.json"))

    def test_performance_valid_against_schema(self):
    	self.assertTrue(valid_against_schema("json/samples/performance.json", "json/performance.json"))
    	self.assertTrue(valid_against_schema("json/samples/performance_minimal.json", "json/performance.json"))

    def test_performance_invalid_against_schema(self):
    	self.assertFalse(valid_against_schema("json/samples/performance_invalid.json", "json/performance.json"))

   	def test_valid_against_metaschema(self):
   		self.assertTrue(valid_against_schema("json/samples/athlete.json", "json/metaschema.json"))
   		self.assertTrue(valid_against_schema("json/samples/combined_performance.json", "json/metaschema.json"))
   		self.assertTrue(valid_against_schema("json/samples/competition.json", "json/metaschema.json"))
   		self.assertTrue(valid_against_schema("json/samples/event.json", "json/metaschema.json"))
   		self.assertTrue(valid_against_schema("json/samples/performance.json", "json/metaschema.json"))

   	def test_invalid_against_metaschema(self):
   		self.assertTrue(valid_against_schema("json/samples/athlete_invalid.json", "json/metaschema.json"))
   		self.assertTrue(valid_against_schema("json/samples/combined_performance_invalid.json", "json/metaschema.json"))
   		self.assertTrue(valid_against_schema("json/samples/competition_invalid.json", "json/metaschema.json"))
   		self.assertTrue(valid_against_schema("json/samples/event_invalid.json", "json/metaschema.json"))
   		self.assertTrue(valid_against_schema("json/samples/performance_invalid.json", "json/metaschema.json"))


if __name__ == '__main__':
    main()
