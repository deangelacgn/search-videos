from search.documents.video import VideoDocument
from elasticsearch_dsl.query import MultiMatch, MatchAll


def retrieve_videos(search_query: str, offset: int, num_items: int) -> list:
    """
    Retrieve videos whose content, description or title are related
    to a search query.
    """
    if search_query is None:
        query = MatchAll()
    else:
        query = MultiMatch(query=search_query,
                           fields=['title', 'transcript', 'description'],
                           fuzziness='AUTO')

    video_search = VideoDocument.search().query(query)

    response = video_search[offset:offset+num_items].execute()
    serialized_response = response.to_dict()
    hits = serialized_response['hits']['hits']
    search_results = sanitize_search_results(hits)

    return search_results


def sanitize_search_results(hits):
    """ Remove unecessary fields returned by ElasticSearch
    """
    search_results = [hit['_source'] for hit in hits]
    for result in search_results:
        result.pop('transcript')
    return search_results
