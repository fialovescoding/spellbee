from pydantic import BaseModel as PydanticBaseModel
from boto3.dynamodb.types import STRING, NUMBER
from typing import List, Dict, Any
from datetime import datetime

from gm_saws.ddb import boto3_wrap, SingleTable, KeyType, IndexType, QueryTerm, QueryConditionType
from core.models import *

class SpellBee_CrudManager:
    def __init__(self, recreate_table: bool = False) -> None:
        # region_name = 'us-east-1'
        table_name = 'spellbee_shared_table'

        # Need high write capacity due to images for primary table
        self.dbe = SingleTable(dyn_resource=boto3_wrap.getDynamoDbResource(local_db=True), table_name=table_name)

        # Create table indices
        
        # pk is used to group related items together, e.g. all data items for a student
        self.dbe.add_key(index=None, indexType=IndexType.MAIN_TABLE, key='pk', type=KeyType.PARTITION_KEY)

        # sk is used to identify each item uniquely
        self.dbe.add_key(index=None, indexType=IndexType.MAIN_TABLE, key='sk', type=KeyType.SORT_KEY, dataType=STRING)

        # gsi-sk are used to create queries based on different criteria

        self.dbe.add_key(index='gsi1', indexType=IndexType.GLOBAL_SECONDARY, key='pk', type=KeyType.PARTITION_KEY)
        self.dbe.add_key(index='gsi1', indexType=IndexType.GLOBAL_SECONDARY, key='gsi1__sk', type=KeyType.SORT_KEY, dataType=STRING)

        # Map Entities to fields

        # TODO: add sort key as word, and gsi1__sk as type#last_seen which gets updated

        # <type>#<Last seen time> for the word used to sort all words for the student - so getting the 1st item using startswith(type), scanIndexForward = False
        self.dbe.map_entity(Word, {
            'pk': (None, ['student_id']),
            'sk': (None, ['data']),
            'gsi1__sk': ('{0}#{1}', ['type', 'last_seen']),
        })
        self.dbe.map_entity(NextWordList, {
            'pk': ('@ClassName#{0}', ['student_id']),
            'sk': (None, ['student_id']),
        })

        if self.dbe.table is None or recreate_table:
            # Create Table
            self.dbe.createTable(forceCreate=True)
        else:
            # Regenerate Reverse map, since table already exists
            self.dbe.gen_reverse_map()


    def put_item(self, entity: PydanticBaseModel):
        # print(f'>>> Saving {entity}')
        self.dbe.put_item(entity)

    def get_next_word(self, student_id: str, word_type: WordType) -> Word | None:
        result = self.dbe.query(
            entity=Word,
            constraints={
                'student_id': QueryTerm(student_id, QueryConditionType.EQ),
                'type': QueryTerm(word_type, QueryConditionType.EQ),
            },
            limit=1
        )

        if result is not None and len(result) == 1:
            word: Word = result[0]
            return word
        else:
            return None
    
    def add_new_word(self, student_id: str, word: str):
        new_word = Word(
            student_id=student_id,
            type=WordType.NEW,
            data=word,
            last_seen=int(datetime.now().timestamp())
        )
        self.dbe.put_item(new_word)
    
    def update_word(self, student_id: str, word: Word, new_type: WordType):
        new_word = Word(
            student_id=student_id,
            type=new_type,
            data=word.data,
            last_seen=int(datetime.now().timestamp())
        )
        self.dbe.put_item(new_word)
    
    def get_next_list(self, student_id: str) -> str:
        result = self.dbe.query(
            entity=NextWordList,
            constraints={
                'student_id': QueryTerm(student_id, QueryConditionType.EQ),
            },
        )

        if result is not None and len(result) == 1:
            return result[0].next_list
        else:
            return None
    
    
    def set_next_list(self, student_id: str, next_list: str):
        e = NextWordList(student_id=student_id, next_list=next_list)
        self.dbe.put_item(e)