# cfn-lambda-import-value
## Description
The `cfn-lambda-import-value` function is `Fn::ImportValue` that support `Region`

## When do you use it
* Import value from other region. (e.g. AWS::CloudFront::Distribution can created in regions other than us-east-1, but AWS::CloudWatch::Alarm for CloudFront can only be created in us-east-1)

## Caution
The function is not subject to existing restriction for safety. You can change the `Export`.

## Deploy
[See here](https://github.com/hixi-hyi/aws-cloudformation-lambda#deploy)

## Usage
```
StackName:
  Type: Custom::Lambda
  Properties:
    ServiceToken: !ImportValue cfn-lambda-import-value:LambdaArn
    Region: ap-northeast-1
    Name: CloudFront:OutputValue
```
## Parameters

### Name
- [Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html#outputs-section-structure-examples)
- ***Required:*** Yes
- ***Update requires:*** Replacement

### Region
- [Docs](https://docs.aws.amazon.com/general/latest/gr/rande.html)
- The region outside the default are also supported.
- Default parameter is `AWS::Region`.
- ***Required:*** No
- ***Update requires:*** Replacement

## ToDO

## Contributing
[See here](https://github.com/hixi-hyi/aws-cloudformation-lambda#contributing)
