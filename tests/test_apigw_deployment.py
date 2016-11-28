#!/usr/bin/python
# TODO: License goes here

import library.apigw_deployment as apigw_deployment
from library.apigw_deployment import ApiGwDeployment
import mock
from mock import patch
from mock import create_autospec
from mock import ANY
import unittest
import boto
from botocore.exceptions import BotoCoreError

class TestApiGwDeployment(unittest.TestCase):

  def setUp(self):
    self.module = mock.MagicMock()
    self.module.check_mode = False
    self.module.exit_json = mock.MagicMock()
    self.module.fail_json = mock.MagicMock()
    self.resource  = ApiGwDeployment(self.module)
    self.resource.client = mock.MagicMock()
    reload(apigw_deployment)

  def test_boto_module_not_found(self):
    # Setup Mock Import Function
    import __builtin__ as builtins
    real_import = builtins.__import__

    def mock_import(name, *args):
      if name == 'boto': raise ImportError
      return real_import(name, *args)

    with mock.patch('__builtin__.__import__', side_effect=mock_import):
      reload(apigw_deployment)
      ApiGwDeployment(self.module)

    self.module.fail_json.assert_called_with(msg='boto and boto3 are required for this module')

  def test_boto3_module_not_found(self):
    # Setup Mock Import Function
    import __builtin__ as builtins
    real_import = builtins.__import__

    def mock_import(name, *args):
      if name == 'boto3': raise ImportError
      return real_import(name, *args)

    with mock.patch('__builtin__.__import__', side_effect=mock_import):
      reload(apigw_deployment)
      ApiGwDeployment(self.module)

    self.module.fail_json.assert_called_with(msg='boto and boto3 are required for this module')

  @patch.object(apigw_deployment, 'boto3')
  def test_boto3_client_properly_instantiated(self, mock_boto):
    ApiGwDeployment(self.module)
    mock_boto.client.assert_called_once_with('apigateway')

  def test_define_argument_spec(self):
    result = ApiGwDeployment._define_module_argument_spec()
    self.assertIsInstance(result, dict)
    self.assertEqual(result, dict(
                     name=dict(required=True, aliases=['stage_name']),
                     rest_api_id=dict(required=True),
                     stage_description=dict(required=False),
                     description=dict(required=False),
                     cache_cluster_enabled=dict(required=False, type='bool', default=False),
                     cache_cluster_size=dict(required=False, choices=['0.5','1.6','6.1','13.5','28.4','58.2','118','237'])
    ))


  @patch.object(apigw_deployment, 'AnsibleModule')
  @patch.object(apigw_deployment, 'ApiGwDeployment')
  def test_main(self, mock_ApiGwDeployment, mock_AnsibleModule):
    mock_ApiGwDeployment_instance      = mock.MagicMock()
    mock_AnsibleModule_instance     = mock.MagicMock()
    mock_ApiGwDeployment.return_value  = mock_ApiGwDeployment_instance
    mock_AnsibleModule.return_value = mock_AnsibleModule_instance

    apigw_deployment.main()

    mock_ApiGwDeployment.assert_called_once_with(mock_AnsibleModule_instance)
    self.assertEqual(1, mock_ApiGwDeployment_instance.process_request.call_count)


if __name__ == '__main__':
    unittest.main()

