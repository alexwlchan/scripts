# terraform

These scripts are all aliases around [Terraform], the infrastructure-as-code tool we use at work.

In some of our Terraform configurations, we use wrapper scripts `run_terraform.sh` instead of invoking `terraform` directly.
This wrapper script fetches API keys for the [Elastic Cloud] and [Auth0] providers, so we don't have to hard-code them or store them locally.
Something like:

```shell
EC_API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id "elastic_cloud/api_key" \
  --output text \
  --query "SecretString")

EC_API_KEY="$EC_API_KEY" terraform "$@"
```

My `tf` scripts will choose whether to run a wrapper script or vanilla `terraform`, so I don't have to think about it.

My scripts are:

<dl>
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/terraform/tf">
      <code>tf</code>
    </a>
  </dt>
  <dd>
    runs <code>terraform</code> (or the wrapper script) with any arguments supplied.
  </dd>
  
  <dt>
    <a href="https://github.com/alexwlchan/scripts/blob/main/terraform/tfi">
      <code>tfi</code>
    </a>
  </dt>
  <dd>
    runs the <a href="https://developer.hashicorp.com/terraform/cli/commands/init"><code>init</code> command</a> plus any extra arguments supplied. e.g. <code>tfi -upgrade</code> becomes <code>terraform init -upgrade</code>
  </dd>
</dl>

[Terraform]: https://www.terraform.io/
[Elastic Cloud]: https://registry.terraform.io/providers/elastic/ec/latest/docs#using-your-api-key-on-the-elastic-cloud-terraform-provider
[Auth0]: https://registry.terraform.io/providers/auth0/auth0/latest/docs#environment-variables