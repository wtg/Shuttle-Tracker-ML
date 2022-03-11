from haversine import haversine, Unit

lyon = (45.7597, 4.8422) # (lat, lon)
paris = (48.8567, 2.3508)

result = haversine(lyon, paris)
print(result)
#>> 392.2172595594006  # in kilometers

haversine(lyon, paris, unit=Unit.MILES)
#>> 243.71201856934454  # in miles

# you can also use the string abbreviation for units:
haversine(lyon, paris, unit='mi')
#>> 243.71201856934454  # in miles

haversine(lyon, paris, unit=Unit.NAUTICAL_MILES)
#>> 211.78037755311516  # in nautical miles