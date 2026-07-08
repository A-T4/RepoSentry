from abc import ABC, abstractmethod
from typing import List
from app.models.findings import Finding

class BaseScanner(ABC):
    """
    The abstract contract for all RepoSentry security scanners.
    """
    
    @abstractmethod
    def scan(self, workspace_path: str) -> List[Finding]:
        """
        Executes the specific security analysis against the cloned repository.
        
        :param workspace_path: The absolute path to the temporary directory containing the code.
        :return: A list of standardized Finding objects.
        """
        pass