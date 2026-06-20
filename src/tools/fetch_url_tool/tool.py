import urllib.request

from tools.base import BaseTool
from tools.fetch_url_tool.model import FetchURLInput



class FetchURLTool(BaseTool):
    
    
    @property
    def name(self) -> str:
        return "fetch_url"
    @property
    def description(self) -> str:
        
        return "fetch url and return content"
    
    @property
    def input_model(self):
        return FetchURLInput

    async def execute(self, **kwargs):

        input = FetchURLInput(**kwargs)        
        try:
            with urllib.request.urlopen(input.url) as content:
                response = content.read().decode('utf-8', errors = "ignore")

            result = {
                "url":input.url,
                "content":response[:5000]
            }
        
        except Exception as e:
            print(e)
            result = {
                "url":input.url,
                "content":"505 Not able to fetch"
            }

        return result
