data "aws_api_gateway_rest_api" "this" {
  name = "main"
}

resource "aws_api_gateway_resource" "this" {
  rest_api_id = data.aws_api_gateway_rest_api.this.id
  parent_id   = data.aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "haze-map"
}


resource "aws_api_gateway_method" "get" {
  rest_api_id   = data.aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.this.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = data.aws_api_gateway_rest_api.this.id
  resource_id             = aws_api_gateway_resource.this.id
  http_method             = aws_api_gateway_method.get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.this.invoke_arn
  lifecycle {
    ignore_changes = [uri] #aws_lambda_function.this.invoke_arn:${stageVariables.lambdaAlias}
  }
}