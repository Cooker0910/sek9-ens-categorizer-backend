from django_countries import countries


def get_country_code_by_name(country_name):
  for code, name in list(countries):
    if name == country_name:
      return code
  return None


def get_country_code_by_code(country_code):
  for code, name in list(countries):
    if code == country_code:
      return name
  return None
