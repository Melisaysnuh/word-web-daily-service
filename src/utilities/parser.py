from typing import Any, Dict
from utilities.custom_types import Definition, Hwi, Meta, DictionaryResponse

def parse_dictionary_response(data: Dict[str, Any]) -> DictionaryResponse:
    meta = Meta(
        id=data['meta']['id'],
        uuid=data['meta']['uuid'],
        sort=int(data['meta']['sort']),
        src=data['meta']['src'],
        section=data['meta']['section'],
        stems=data['meta']['stems'],
        offensive=data['meta']['offensive']
    )
    hwi = Hwi(hw=data['hwi']['hw'])
    shortdef = data.get('shortdef', [])
    date = data.get('date', '')

    # Extract nested definition text
    definitions: list[Definition] = []
    for def_block in data.get('def', []):
        for sseq_group in def_block.get('sseq', []):
            for sense_group in sseq_group:
                if sense_group[0] == 'sense':
                    sense_data = sense_group[1]
                    for dt_entry in sense_data.get('dt', []):
                        if dt_entry[0] == 'text':
                            text = dt_entry[1].replace('{bc}', '').strip()
                            definitions.append(Definition(text=text))

    fl: str = data.get('fl')
    if not fl:
        cxs = data.get('cxs')
        print(f"[parsing_dictionary_response] cxs is {cxs}")
        if cxs and isinstance(cxs, list):
            fl = ', '.join(cxs) # type: ignore
        else:
            fl = 'unknown'

    return DictionaryResponse(
        meta=meta,
        hwi=hwi,
        fl = fl,
        shortdef=shortdef,
        date=date,
        definitions=definitions
    )

