from samudra import tools
from tests import mocks


def test_parse_dataframe():
    data = mocks.TestLemma()
    dataframe = data.from_excel
    new_data = tools.parse_dataframe(dataframe)
    schema = data.to_schema
    assert new_data[0].nama == schema.nama
    assert new_data[0].konsep[0].golongan == schema.konsep[0].golongan
    assert new_data[0].konsep[0].keterangan == schema.konsep[0].keterangan
    assert new_data[0].konsep[0].cakupan == schema.konsep[0].cakupan
    assert new_data[0].konsep[0].kata_asing == schema.konsep[0].kata_asing
