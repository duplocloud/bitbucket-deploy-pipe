import requests
from bitbucket_pipes_toolkit import Pipe, yaml, get_variable, get_logger

# some global vars
REQUESTS_DEFAULT_TIMEOUT = 10

# Required vars for updating a service
schema = {
  'DUPLO_TOKEN': {'required': True, 'type': 'string'},
  'DUPLO_HOST': {'required': True, 'type': 'string'},
  'TENANT': {'required': True, 'type': 'string'},
  'SERVICE': {'required': True, 'type': 'string'},
  'IMAGE': {'required': True, 'type': 'string'}
}

logger = get_logger()

class DuploDeploy(Pipe):
  """Duplo Deploy Pipe"""
  url = None
  headers = None
  service = None
  image = None
  tenant_name = None

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    token = self.get_variable("DUPLO_TOKEN")
    self.url = self.get_variable("DUPLO_HOST")
    self.service = self.get_variable("SERVICE")
    self.tenant_name = self.get_variable("TENANT")
    self.image = self.get_variable("IMAGE")
    self.headers = {
      'Content-Type': 'application/json',
      'Authorization': f"Bearer {token}"
    }
  
  def get_tenant_id(self):
    """Get Tenant ID
    Retrieves the tennats ID based on the name variable.
    """
    try:
      response = requests.get(
        url=f"{self.url}/adminproxy/GetTenantNames",
        headers=self.headers,
        timeout=REQUESTS_DEFAULT_TIMEOUT
      )
      tenant = [t for t in response.json() if t["AccountName"] == self.tenant_name][0]
      return tenant["TenantId"]
    except Exception as e:
      self.fail(f"Could find tenant named {self.tenant_name}")

  def get_allocation_tags(self, tenant_id):
    try:
      response = requests.get(
        url=f"{self.url}/subscriptions/{tenant_id}/GetReplicationControllers",
        headers=self.headers,
        timeout=10
      )
      service = [s for s in response.json() if s["Name"] == self.service][0]
      return service["Template"]["AllocationTags"]
    except Exception as e:
      self.fail(f"Could find service named {self.service}")

  def update_image(self):
    try:
      tenant_id = self.get_tenant_id()
      allocation_tags = self.get_allocation_tags(tenant_id)
      data = {
        "Name": self.service,
        "Image": self.image,
        "AllocationTags": allocation_tags
      }
      response = requests.post(
        url=f"{self.url}/subscriptions/{tenant_id}/ReplicationControllerChange",
        headers=self.headers,
        json=data,
        timeout=REQUESTS_DEFAULT_TIMEOUT
      )
      if 200 <= response.status_code <= 299:
          self.success(f"Updated {self.service} image to {self.image}")
      else:
          self.fail(f"Unable to update {self.service} image to {self.image}")
    except requests.exceptions.Timeout as error:
      self.fail(error)
    except requests.ConnectionError as error:
      self.fail(error)

  def run(self):
    super().run()
    logger.info(f"Updating {self.service} in {self.tenant_name}")
    self.update_image()

if __name__ == '__main__':
  with open('/pipe.yml', 'r') as metadata_file:
    metadata = yaml.safe_load(metadata_file.read())
  duplo_deploy = DuploDeploy(pipe_metadata=metadata, schema=schema)
  duplo_deploy.run()