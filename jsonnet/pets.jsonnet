local Pet(name='', category='') = (
  local categories = [
    'dog',
    'spider',
  ];

  assert name != '' : 'name required';
  assert std.member(categories, category) : 'unknown category "' + category + '"';

  {
    name: name,
    category: category,
  }

);

local Dog(name='', birthday='') = Pet(category='dog', name=name);

local Spider(name='') = Pet(category='spider', name=name);

local dogs = [
  Dog(name='Ollie'),
  Dog(name='Ziggy'),
  Dog(name='Minnie'),
];

local spiders = [
  Spider(name='Spidey'),
  Spider(name='Karta'),
  Spider(name='Glassy'),
  Spider(name='Leo'),
  Spider(name='Spiker'),
  Spider(name='Venom'),
  Spider(name='Tex'),
  Spider(name='Tio'),
  Spider(name='Lalo'),
];

dogs + spiders
