from __future__ import absolute_import, division, print_function
import sys
class Serverless:
    """
    Serverless
    """

    def __init__(self, debug=False):
        '''
        Initialize
        :param debug:
        '''
        self.debug = debug

        if self.debug:
            print('init')

    def perform_transform(self, cfn_hash):
        '''
        ???
        :param cfn_hash:
        :return:
        '''
        if self.debug:
            print('perform_transform')
            print('cfn_hash: '+str(cfn_hash))
        resources = {}
        sys.exit(1)
        resources = cfn_hash['Resources']
        if self.debug:
            print('resources: '+str(resources))
        # resources = cfn_hash['Resources'].clone

        for resource in resources:
            if self.debug:
                print(resource)
        # resources.each do |resource_name, resource|
        #  next unless resource['Type'].eql? 'AWS::Serverless::Function'
        #  replace_serverless_function cfn_hash, resource_name



    def instance(self):
          '''
          ???
          :return:
          '''
          if self.debug:
            print('instance')
          # FIXME
          sys.exit(1)

    def bucket_from_uri(self, uri):
          '''
          ???
          :param uri:
          :return:
          '''
          if self.debug:
            print('bucket_from_uri')
          # FIXME
          sys.exit(1)

    def object_key_from_uri(self, uri):
          '''
          ???
          :param uri:
          :return:
          '''
          if self.debug:
            print('object_key_from_uri')
          sys.exit(1)

    def is_s3_uri(self, uri):
          '''
          ???
          :param uri:
          :return:
          '''
          if self.debug:
            print('is_s3_uri')

          sys.exit(1)

    def replace_serverless_function(self, cfn_hash, resource_name):
          '''
          ???
          :param cfn_hash:
          :param resource_name:
          :return:
          '''
          if self.debug:
            print('replace_serverless_function')
          # FIXME
          sys.exit(1)
          # resource = cfn_hash['Resources'][resource_name]
          # code_uri = resource['Properties']['CodeUri']

          # lambda_fn_params = {
          #  handler: resource['Properties']['Handler'],
          #  runtime: resource['Properties']['Runtime']
          # }
          # if is_s3_uri? code_uri
          #  lambda_fn_params[:code_bucket] = bucket_from_uri code_uri
          #  lambda_fn_params[:code_key] = object_key_from_uri code_uri
          # end
          # cfn_hash['Resources'][resource_name] = \
          #  lambda_function lambda_fn_params

          # cfn_hash['Resources']['FunctionNameRole'] = function_name_role

    def function_name_role(self):
          '''
          ???
          :return:
          '''
          if self.debug:
            print('function_name_role')
          # FIXME
          sys.exit(1)
          #  {
          #    'Type' => 'AWS::IAM::Role',
          #    'Properties' => {
          #      'ManagedPolicyArns' =>
          #      ['arn:aws:iam::aws:policy/service-role/' \
          #        'AWSLambdaBasicExecutionRole'],
          #      'AssumeRolePolicyDocument' => {
          #        'Version' => '2012-10-17',
          #        'Statement' => [{
          #          'Action' => ['sts:AssumeRole'], 'Effect' => 'Allow',
          #          'Principal' => { 'Service' => ['lambda.amazonaws.com'] }
          #        }]
          #      }
          #    }
          #  }

    def lambda_function(self, handler, runtime, code_bucket=None, code_key=None):
          '''
          ???
          :param handler:
          :param runtime:
          :param code_bucket:
          :param code_key:
          :return:
          '''
          if self.debug:
            print('lambda_function')
          # FIXME
          sys.exit(1)
          # fn_resource = \
          #    {'Type' = > 'AWS::Lambda::Function',
          #                'Properties' = > {
          #    'Handler' = > handler,
          #                  'Role' = > {'Fn::GetAtt' = > % w[FunctionNameRole
          # Arn]},
          # 'Runtime' = > runtime
          # }}
          # if code_bucket & & code_key
          #    fn_resource['Properties']['Code'] = {
          #        'S3Bucket' = > code_bucket,
          #                       'S3Key' = > code_key
          #    }
          #    end