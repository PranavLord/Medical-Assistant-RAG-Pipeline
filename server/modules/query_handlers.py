from logger import logger

def query_chain(chain,user_input:str):
    try:
        logger.debug(f"Running chain for input: {user_input}")
        result=chain({"query":user_input})
        logger.debug(f"Chain response:{result['result']}")
        return result["result"]
    except Exception as e:
        logger.exception("Error on query chain")
        raise