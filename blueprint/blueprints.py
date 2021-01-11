import typing

from blueprint.core.field import Field
from blueprint.core import BluePrint


class Character(BluePrint):
    level = Field(
        verbose_name='Level',
        data_type='int',
        required=True,
        default=1,
    )
    star = Field(
        verbose_name='Star',
        data_type='int',
        required=True,
        default=1,
    )
    exp = Field(
        verbose_name='Experience',
        data_type='int',
        required=True,
        default=0,
    )
    config_id = Field(
        verbose_name='Configuration ID',
        data_type='string',
        required=True,
    )

    class Meta:
        config_key = 'character'
        instance_id_template = '{config_id}_{random_string}_{create_ts}'
        single_instance = True  # 1 config to multiple instances ?


class Architecture(BluePrint):
    pass


class Role(BluePrint):
    server_id = Field(
        verbose_name='Server ID',
        data_type='string',
        required=True,
    )
    role_id = Field(
        verbose_name='Role ID',
        data_type='string',
        required=True,
    )
    characters = Field(
        verbose_name='Characters',
        data_type=Character,
        container='map',
        container_config={
            'group_by': ['instance_id']
        }
    )

    class Meta:
        instance_id_template = 'role_{server_id}_{role_id}'

    def add_character(self, character: Character):
        cls_dict = self.__class__.__dict__
        characters_field: Field = cls_dict.get('characters')
        group_by: typing.List[str] = characters_field.container_config.get('group_by')
        print(characters_field.name)


if __name__ == '__main__':
    role = Role(server_id='s1', role_id='r10001')
    role.save()

    character = Character(config_id='20001')
    character.level += 1
    character.save()

    role.add_character(character)
