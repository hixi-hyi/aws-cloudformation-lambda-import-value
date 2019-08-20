from unittest import TestCase
from moto import mock_cloudformation
from moto import mock_s3
from src.index import ImportValue
import cfntest
import boto3


TEMPLATE = """
AWSTemplateFormatVersion: 2010-09-09
Description: Simple test CF template for moto_cloudformation
Resources:
    Bucket:
        Type: AWS::S3::Bucket
        Properties:
            BucketName: !Sub ${AWS::StackName}-bucket
Outputs:
    OutputBucketName:
        Value: !Ref Bucket
        Export:
            Name: !Ref AWS::StackName
"""


class TestScenario(TestCase):
    @mock_cloudformation
    @mock_s3
    def test_default(self):
        STACK_NAME = 'test-default-stack'
        client = boto3.client('cloudformation')
        client.create_stack(StackName=STACK_NAME, TemplateBody=TEMPLATE)
        context = cfntest.get_context()
        create_event = cfntest.get_create_event({"Name": STACK_NAME})
        update_event = cfntest.get_update_event({"Name": STACK_NAME}, cfntest.get_properties(create_event))
        delete_event = cfntest.get_delete_event(cfntest.get_properties(update_event), cfntest.get_properties(create_event))

        if True:
            c = ImportValue(create_event, context)
            c.run()
            self.assertEqual(c.response.get_data('Value'), "test-default-stack-bucket")

        if True:
            c = ImportValue(update_event, context)
            c.run()
            self.assertEqual(c.response.get_data('Value'), "test-default-stack-bucket")

        if True:
            c = ImportValue(delete_event, context)
            c.run()

    @mock_cloudformation
    @mock_s3
    def test_pagination(self):
        STACK_NAME = 'test-pagination-stack'
        client = boto3.client('cloudformation')
        client.create_stack(StackName=STACK_NAME, TemplateBody=TEMPLATE)
        for i in range(100):
            client.create_stack(StackName='{}-{}'.format(STACK_NAME, i), TemplateBody=TEMPLATE)
        context = cfntest.get_context()
        create_event = cfntest.get_create_event({"Name": STACK_NAME})
        update_event = cfntest.get_update_event({"Name": STACK_NAME}, cfntest.get_properties(create_event))
        delete_event = cfntest.get_delete_event(cfntest.get_properties(update_event), cfntest.get_properties(create_event))

        if True:
            c = ImportValue(create_event, context)
            c.run()
            self.assertEqual(c.response.get_data('Value'), "test-pagination-stack-bucket")

        if True:
            c = ImportValue(update_event, context)
            c.run()
            self.assertEqual(c.response.get_data('Value'), "test-pagination-stack-bucket")

        if True:
            c = ImportValue(delete_event, context)
            c.run()

    @mock_cloudformation
    def test_error_not_found(self):
        context = cfntest.get_context()
        create_event = cfntest.get_create_event({"Name": 'hogehoge'})

        if True:
            c = ImportValue(create_event, context)
            with self.assertRaises(Exception):
                c.run()
