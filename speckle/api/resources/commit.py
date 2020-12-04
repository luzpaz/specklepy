from typing import Optional, List
from gql import gql
from pydantic.main import BaseModel
from speckle.api.resource import ResourceBase
from speckle.api.models import Commit


NAME = "commit"
METHODS = []


class Resource(ResourceBase):
    """API Access class for commits"""

    def __init__(self, me, basepath, client) -> None:
        super().__init__(
            me=me, basepath=basepath, client=client, name=NAME, methods=METHODS
        )
        self.schema = Commit

    def get(self, stream_id: str, commit_id: str) -> Commit:
        """
        Gets a commit given a stream and the commit id

        Arguments:
            stream_id {str} -- the stream where we can find the commit
            commit_id {str} -- the id of the commit you want to get

        Returns:
            Commit -- the retrieved commit object
        """
        query = gql(
            """
            query Commit($stream_id: String!, $commit_id: String!) {
                stream(id: $stream_id) {
                    commit(id: $commit_id) {
                        id
                        referencedObject
                        message
                        authorName
                        authorId
                        createdAt
                    }
                }
            }
            """
        )
        params = {"stream_id": stream_id, "commit_id": commit_id}

        return self.make_request(
            query=query, params=params, return_type=["stream", "commit"]
        )

    def list(self, stream_id: str, limit: int = 10) -> List[Commit]:
        """
        Get a list of commits on a given stream

        Arguments:
            stream_id {str} -- the stream where the commits are
            limit {int} -- the maximum number of commits to fetch (default = 10)

        Returns:
            List[Commit] -- a list of the most recent commit objects
        """
        query = gql(
            """
            query Commits($stream_id: String!, $limit: Int!) {
                stream(id: $stream_id) {
                    commits(limit: $limit) {
                        items {
                            id
                            message
                            authorName
                            authorId
                            createdAt
                            referencedObject
                        }
                    }
                }
            }
            """
        )
        params = {"stream_id": stream_id, "limit": limit}

        return self.make_request(
            query=query, params=params, return_type=["stream", "commits", "items"]
        )

    def create(
        self,
        stream_id: str,
        object_id: str,
        branch_name: str = "main",
        message: str = "",
    ):
        """
        docstring
        """
        raise NotImplementedError

    def update(self, stream_id: str, commit_id: str, message: str) -> bool:
        """
        docstring
        """
        raise NotImplementedError

    def delete(self, stream_id: str, commit_id: str) -> bool:
        """
        docstring
        """
        raise NotImplementedError