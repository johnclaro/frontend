import sys
import logging
import copy
import io

import requests


class Netlify:

    def __init__(
        self, 
        access_token: str='', 
        scheme: str='https', 
        host: str='api.netlify.com', 
        version: str='/api/v1/'
    ):
        """The primary Netlify class .

            :param access_token: Personal access token generated by Netlify.
            :param scheme: Scheme of Netlify's API url.
            :param host: Host of Netlify's API url.
            :param version: Version of Netlify's API url.
        """
        self.access_token = access_token
        self.scheme = scheme
        self.host = host
        self.version = version
        self.url = f'{scheme}://{host}{version}'
        if self.access_token:
            self.headers = {'Authorization': f'Bearer {access_token}'}
        else:
            self.headers = {}

    def create_site(self, name: str) -> requests.models.Response:
        """Create a site in Netlify.

            :param name: Name of site.
        """
        url = f'{self.url}/sites'
        data = {'name': name}
        return requests.post(url, data=data, headers=self.headers)

    def get_sites(self) -> requests.models.Response:
        """Get list of sites in Netlify."""
        url = f'{self.url}/sites'
        return requests.get(url, headers=self.headers)

    def get_site_id(self, name: str) -> str:
        """Get the ID of a site by its name.

            :param name: Name of site.
        """
        site_id = None
        sites = self.get_sites().json()
        for site in sites:
            if site['name'] == name:
                site_id = site['id']
                break

        if not site_id:
            logging.warning(f"Site '{name}' not found.")

        return site_id

    def deploy_site(
        self,
        site_id: str,
        file_digest: dict=None,
        zip_file: io.BufferedReader=None
    ) -> requests.models.Response:
        """Deploy new or updated version of website.

        Netlify supports two ways of doing deploys:

        1. Sending a digest of all files in your deploy and then uploading \t
            any files Netlify doesn't already have on its storage servers.

        2. Sending a zipped website and letting Netlify unzip and deploy.

        The former is the recommended approach by Netlify.

            :param site_id: Site ID of a site.
            :param file_digest: Digest of file paths and SHA1 of file paths.
            :param zip_file: Content of zip file.
        """
        headers = copy.deepcopy(self.headers)
        url = f'{self.url}/{site_id}/deploys'

        if zip_file or file_digest:
            if zip_file:
                if type(zip_file) == io.BufferedReader:
                    headers['Content-Type'] = 'application/zip'
                    data = zip_file
                else:
                    sys.exit('Zip file must be of type BufferedReader')

            if file_digest:
                if type(file_digest) == dict:
                    data = file_digest
                else:
                    sys.exit('File digest must be of type dict')
        else:
            sys.exit('You must supply a zip file or a file digest')

        return requests.post(url, headers=headers, data=data)
