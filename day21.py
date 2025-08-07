from util import read_input

raw = read_input(21)
foods = raw.strip().splitlines()

possible_ingredients_by_allergen = {}
all_ingredients = set()
for food in foods:
  ingregients_list, allergens = food.split(' (contains ')
  ingredients = set(ingregients_list.split())
  all_ingredients |= ingredients
  allergens = allergens.rstrip(')')
  allergens = set(allergens.split(', '))
  for allergen in allergens:
    if allergen not in possible_ingredients_by_allergen:
      possible_ingredients_by_allergen[allergen] = ingredients.copy() # without this copyy, some allergents share the same instance of the ingredients set. That is not right.
    else:
      possible_ingredients_by_allergen[allergen] &= ingredients # ampersand means intersection



# what foodstuffs are not in any  of the eligibility lists?
ingredients_with_no_possible_allergens = all_ingredients.copy()
for allergen, foodstuffs in possible_ingredients_by_allergen.items():
    ingredients_with_no_possible_allergens -= foodstuffs

# count how many occurances of these are in the input
count = 0
for food in raw.strip().splitlines():
  ingredients = food.split(' (contains',1)[0].split(' ')
  count += sum(1 for ing in ingredients if ing in ingredients_with_no_possible_allergens)



assert count < 2563, "My first try was wrong due to an implementation error"
assert count == 2461, "This is the right answer!"


# part 2 resolve allocations
allocations = {}
while any(len(v)==1 for k,v in possible_ingredients_by_allergen.items()):
  to_allocate = next((k for k,v in possible_ingredients_by_allergen.items() if len(v)==1))
  ingredient = possible_ingredients_by_allergen[to_allocate].pop()
  allocations[to_allocate] = ingredient
  for k,v in possible_ingredients_by_allergen.items():
    v -= {ingredient}
  del possible_ingredients_by_allergen[to_allocate]

assert len(possible_ingredients_by_allergen) == 0, "There should be no allergens left to allocate"
canonical_dangerous_ingredient_list = ','.join(
    ingredient for _, ingredient in sorted(allocations.items(), key=lambda x: x[0])
)
assert canonical_dangerous_ingredient_list == 'ltbj,nrfmm,pvhcsn,jxbnb,chpdjkf,jtqt,zzkq,jqnhd'