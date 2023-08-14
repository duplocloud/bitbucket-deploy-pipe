# DuploCloud Pipelines Pipe: Deploy  

Updates a services image tag on DuploCloud. 

## YAML Definition  

```yaml
- pipe: docker://duplocloud/bitbucket-deploy-pipe:1.0.0
  variables:
    DUPLO_TOKEN: '<string>'
    DUPLO_HOST: '<string>'
    TENANT: '<string>'
    SERVICE: '<string>'
    IMAGE: '<string>'
```

## Variables  

| Variable | Usage |  
| -------- | ----- |  
| DUPLO_TOKEN | Auth token for Duplo |  
| DUPLO_HOST | The domain of your Duplo instance |  
| TENANT | The tenant where the service is in |  
| SERVICE | The name of the service to update |  
| IMAGE | The new image of the service. | 
| SLACK_WEBHOOK | Webhook for pre/post deploy notifications. Blank for no notifications. |
| NOTIF_REGION | Cloud region to mention in the message. |
| NOTIF_ACCOUNT | Cloud account to mention in the message. |
| NOTIF_ENV | Cloud env to mention in the message. |
| BITBUCKET_REPO_FULL_NAME | Repo name used in build link. |
| BITBUCKET_BUILD_NUMBER | Build number used in build link. |

## Prerequisites  

To make an update to a service you will need a duplo token. 