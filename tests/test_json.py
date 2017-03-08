"""
This file covers testing validity of JSON schemata, plus the fields in the
schemta themselves.
"""
import sys, os
from pprint import pprint
import jsonschema
from jsonschema.exceptions import SchemaError, ValidationError
from unittest import TestCase, main
from athlib.utils import _rootdir, localpath, schema_valid, valid_against_schema

class JsonSchemaValidityTests(TestCase):

    def test_metaschema_valid(self):
        self.assertTrue(schema_valid("json/metaschema.json"))
        self.assertTrue(schema_valid("json/metaschema.json",
                                     validator=jsonschema.Draft4Validator))

    def test_athlete_schema_valid(self):
        # Required properties not valid in V3
        with self.assertRaises(SchemaError):
            schema_valid("json/athlete.json", expect_failure=True)

        self.assertTrue(schema_valid("json/athlete.json",
                                     validator=jsonschema.Draft4Validator))

    def test_combined_performance_schema_valid(self):
        # Required properties not valid in V3
        with self.assertRaises(SchemaError):
            schema_valid("json/combined_performance.json",
                         expect_failure=True)

        self.assertTrue(schema_valid("json/combined_performance.json",
                                     validator=jsonschema.Draft4Validator))

    def test_competition_schema_valid(self):
        # Required properties not valid in V3
        with self.assertRaises(SchemaError):
            schema_valid("json/competition.json", expect_failure=True)

        self.assertTrue(schema_valid("json/competition.json",
                                     validator=jsonschema.Draft4Validator))

    def test_event_schema_valid(self):
        # Required properties not valid in V3
        with self.assertRaises(SchemaError):
            schema_valid("json/event.json", expect_failure=True)

        self.assertTrue(schema_valid("json/event.json",
                                     validator=jsonschema.Draft4Validator))

    def test_performance_schema_valid(self):
        self.assertTrue(schema_valid("json/performance.json"))
        self.assertTrue(schema_valid("json/performance.json",
                                     validator=jsonschema.Draft4Validator))

    def test_race_schema_valid(self):
        self.assertTrue(schema_valid("json/race.json"))
        self.assertTrue(schema_valid("json/race.json",
                                     validator=jsonschema.Draft4Validator))

    def test_athlete_valid_against_schema(self):
        self.assertTrue(valid_against_schema(
            "json/samples/athlete.json",
            "json/athlete.json")
        )
        self.assertTrue(valid_against_schema(
            "json/samples/athlete_minimal.json",
            "json/athlete.json")
        )

    def test_athlete_invalid_against_schema(self):
        with self.assertRaises(ValidationError):
            valid_against_schema("json/samples/athlete_invalid.json",
                                 "json/athlete.json",
                                 expect_failure=True)

    def test_combined_performance_valid_against_schema(self):
        self.assertTrue(valid_against_schema(
            "json/samples/combined_performance.json",
            "json/combined_performance.json")
        )
        self.assertTrue(valid_against_schema(
            "json/samples/combined_performance_minimal.json",
            "json/combined_performance.json")
        )

    def test_combined_performance_invalid_against_schema(self):
        with self.assertRaises(ValidationError):
            valid_against_schema(
                "json/samples/combined_performance_invalid.json",
                "json/combined_performance.json",
                expect_failure=True
            )

        with self.assertRaises(ValidationError):
            valid_against_schema(
                "json/samples/combined_performance_invalid2.json",
                "json/combined_performance.json",
                expect_failure=True
            )

    def test_competition_valid_against_schema(self):
        self.assertTrue(valid_against_schema(
            "json/samples/competition.json",
            "json/competition.json")
        )
        self.assertTrue(valid_against_schema(
            "json/samples/competition_minimal.json",
            "json/competition.json")
        )

    def test_competition_invalid_against_schema(self):
        with self.assertRaises(ValidationError):
            valid_against_schema("json/samples/competition_invalid.json",
                                 "json/competition.json",
                                 expect_failure=True)

    def test_event_valid_against_schema(self):
        self.assertTrue(valid_against_schema("json/samples/event.json",
                                             "json/event.json"))
        self.assertTrue(valid_against_schema("json/samples/event_minimal.json",
                                             "json/event.json"))

    def test_event_invalid_against_schema(self):
        with self.assertRaises(ValidationError):
            valid_against_schema("json/samples/event_invalid.json",
                                 "json/event.json",
                                 expect_failure=True)

    def test_performance_valid_against_schema(self):
        self.assertTrue(valid_against_schema("json/samples/performance.json",
                                             "json/performance.json"))
        self.assertTrue(valid_against_schema(
            "json/samples/performance_minimal.json",
            "json/performance.json")
        )

    def test_performance_invalid_against_schema(self):
        with self.assertRaises(ValidationError):
            valid_against_schema("json/samples/performance_invalid.json",
                                 "json/performance.json",
                                 expect_failure=True)

        with self.assertRaises(ValidationError):
            valid_against_schema("json/samples/performance_invalid2.json",
                                 "json/performance.json",
                                 expect_failure=True)

    def test_race_valid_against_schema(self):
        self.assertTrue(valid_against_schema(
            "json/samples/race_iffleymiles_2016_600mA.json",
            "json/race.json"))
        self.assertTrue(valid_against_schema(
            "json/samples/race_iffleymiles_2016_600mB.json",
            "json/race.json"))
        self.assertTrue(valid_against_schema(
            "json/samples/race_iffleymiles_2016_mileA.json",
            "json/race.json"))
        self.assertTrue(valid_against_schema(
            "json/samples/race_iffleymiles_2016_mileB.json",
            "json/race.json"))

    def test_race_invalid_against_schema(self):
        with self.assertRaises(ValidationError):
            valid_against_schema(
                "json/samples/race_invalid_athlete_internal.json",
                "json/race.json",
                expect_failure=True)

        with self.assertRaises(ValidationError):
            valid_against_schema(
                "json/samples/race_invalid_athlete_external.json",
                "json/race.json",
                expect_failure=True)

        with self.assertRaises(ValidationError):
            valid_against_schema("json/samples/race_invalid_position.json",
                                 "json/race.json",
                                 expect_failure=True)

        with self.assertRaises(ValidationError):
            valid_against_schema("json/samples/race_invalid_result.json",
                                 "json/race.json",
                                 expect_failure=True)

    def test_valid_against_metaschema(self):
        self.assertTrue(valid_against_schema("json/samples/athlete.json",
                                             "json/metaschema.json"))
        self.assertTrue(valid_against_schema(
            "json/samples/combined_performance.json",
            "json/metaschema.json")
        )
        self.assertTrue(valid_against_schema("json/samples/competition.json",
                                             "json/metaschema.json"))
        self.assertTrue(valid_against_schema("json/samples/event.json",
                                             "json/metaschema.json"))
        self.assertTrue(valid_against_schema("json/samples/performance.json",
                                             "json/metaschema.json"))

    def test_invalid_against_metaschema(self):
        with self.assertRaises(ValidationError):
            valid_against_schema("json/samples/athlete_invalid.json",
                                 "json/metaschema.json",
                                 expect_failure=True)

        with self.assertRaises(ValidationError):
            valid_against_schema(
                "json/samples/combined_performance_invalid.json",
                "json/metaschema.json",
                expect_failure=True)

        with self.assertRaises(ValidationError):
            valid_against_schema(
                "json/samples/competition_invalid.json",
                "json/metaschema.json",
                expect_failure=True)

        with self.assertRaises(ValidationError):
            valid_against_schema("json/samples/event_invalid.json",
                                 "json/metaschema.json",
                                 expect_failure=True)

        with self.assertRaises(ValidationError):
            valid_against_schema("json/samples/performance_invalid.json",
                                 "json/metaschema.json",
                                 expect_failure=True)


if __name__ == '__main__':
    main()
