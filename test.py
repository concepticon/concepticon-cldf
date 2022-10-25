
def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)
    #
    # FIXME: check ParameterTable Replacement_ID!
    # also: cldf.add_foreign_key('relationtypes.csv', 'Inverse_ID', 'relationtypes.csv', 'ID')
    #
