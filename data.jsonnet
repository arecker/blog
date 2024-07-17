local Spider(personal='', common='', scientific='', image='', acquired=[], deceased=null, endemic='') = (
  assert personal != '' : 'name required';
  assert common != '' : 'common required';
  assert scientific != '' : 'scientific required';
  assert image != '' : 'image required';
  assert endemic != '' : 'endemic required';
  assert std.length(acquired) == 3 : 'acquired should have length 3';

  std.prune({
    personal: personal,
    common: common,
    scientific: scientific,
    image: image,
    acquired: acquired,
    endemic: endemic,
    deceased: deceased,
  })
);

local spiders = [
  Spider(
    personal='Spidey',
    common='Mexican Rose Grey',
    scientific='Tlitocatl verdezi',
    image='2023-06-26-spidey.jpg',
    acquired=[5, 7, 2021],
    endemic='Mexico - Southern Guerrero and eastern Oaxaca',
  ),
  Spider(
    personal='Karta',
    common='Mexican Red Knee',
    scientific='Brachypelma hamorii',
    image='2023-05-26-karta.jpg',
    acquired=[5, 7, 2021],
    endemic='Mexico - Colima, Jalisco, and Michoacán',
  ),
  Spider(
    personal='Glassy',
    common='Curly Hair',
    scientific='Tliltocatl albopilosus',
    image='2023-06-19-glassy.jpg',
    acquired=[16, 7, 2021],
    endemic='Nicaragua and Costa Rica',
  ),
  Spider(
    personal='Leo',
    common='Green Bottle Blue',
    scientific='Chromatopelma cyaneopubescens',
    image='2023-09-12-leo.jpg',
    acquired=[6, 10, 2021],
    endemic='Northern Venezuela (coastal)',
  ),
  Spider(
    personal='Spiker',
    common='Chaco Golden Knee',
    scientific='Grammostola pulchripes ',
    image='2023-11-11-spiker-rehouse.jpg',
    acquired=[6, 10, 2021],
    endemic='Argentina and Paraguay (grasslands)',
  ),
  Spider(
    personal='Venom',
    common='Brazilian Black',
    scientific='Grammostola pulchra',
    image='2023-08-16-venom.jpg',
    acquired=[6, 10, 2021],
    endemic='Brazil and Uruguay (grasslands)'
  ),
  Spider(
    personal='Tex',
    common='Texas Brown',
    scientific='Aphonopelma hentzi',
    image='2023-06-22-tex.jpg',
    acquired=[5, 1, 2022],
    deceased=[30, 5, 2024],
    endemic='Colorado, Kansas, Missouri, New Mexico, Oklahoma, Arkansas, Texas, and Louisiana',
  ),
  Spider(
    personal='Tio',
    common='Guatemalen Tiger Rump',
    scientific='Davus pentaloris',
    image='2022-08-24-tio.jpg',
    acquired=[14, 1, 2022],
    endemic='Mexico and Guatemala',
  ),
  Spider(
    personal='Lalo',
    common='Brazilian Salmon Pink Bird-eater',
    scientific='Lasiodora parahybana',
    image='2022-06-07-lalo.jpg',
    acquired=[7, 6, 2022],
    deceased=[9, 9, 2022],
    endemic='Brazil (forest)',
  ),
  Spider(
    personal='Beans',
    common='Brazilian White Knee',
    scientific='Acanthoscurria geniculata',
    image='2023-04-04-beans.jpg',
    acquired=[10, 8, 2022],
    endemic='Northern Brazil',
  )
];

{
  'spiders.json': spiders,
}
