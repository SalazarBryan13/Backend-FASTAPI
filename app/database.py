import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import Client, create_client
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


@lru_cache(maxsize=1)
def get_supabase() -> Client:
	"""Initialize and cache the Supabase client.

	Reads `SUPABASE_URL` and `SUPABASE_KEY` from environment variables.
	"""
	url = os.getenv("SUPABASE_URL")
	key = os.getenv("SUPABASE_KEY")
	if not url or not key:
		raise RuntimeError(
			"Missing SUPABASE_URL or SUPABASE_KEY. Set them in environment or .env"
		)
	try:
		#creat supabase client
		supabase_client: Client = create_client(url,key)
		return supabase_client
	except Exception as e:
		logger.error(f"Error initializing Supabase client: {e}")
		raise RuntimeError("Failed to initialize Supabase client.") from e
	

	