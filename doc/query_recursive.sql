WITH RECURSIVE
  narrower(n) AS (
    SELECT cldf_id FROM ParameterTable WHERE cldf_name = 'BROTHER'
    UNION
    SELECT cldf_sourceParameterReference FROM ParameterNetwork, narrower
     WHERE ParameterNetwork.cldf_targetParameterReference=narrower.n AND ParameterNetwork.relation = 'broader'
  )
SELECT cldf_id, cldf_name FROM ParameterTable
 WHERE cldf_id IN narrower;