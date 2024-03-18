import challenger_data
import common
import pandas as pd


api_key = common.api_key

challengerData = challenger_data.get_challenger_data(api_key)
# print(challengerData.columns)
# print(challengerData['summonerId'])

puuid = challenger_data.get_puuids(api_key, challengerData)

# unique_match_ids = set()
# matchId = challenger_data.get_match_ids(api_key, puuid)
# for ids in matchId.values():
#     unique_match_ids.update(ids)
#
# print("Unique Match IDs:")
# for match_id in sorted(unique_match_ids):
#     print(match_id)
#
#


