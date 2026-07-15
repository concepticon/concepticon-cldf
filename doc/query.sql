SELECT c.cldf_id, ft.cldf_form, pt.cldf_name FROM
  ContributionTable as ct,
  `concepts.csv` as c,
  FormTable as ft,
  ParameterTable as pt
WHERE
  ct.cldf_id = c.cldf_contributionReference AND
  ft.Concept_ID = c.cldf_id AND
  pt.cldf_id = ft.cldf_parameterReference AND
  ct.cldf_id = 'Swadesh-1955-100'
ORDER BY
  c.`Index`