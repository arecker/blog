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
  // Lol
  // Spider(
  //   personal='Lassie',
  //   common='Brazilian Salmon Pink Bird-eater',
  //   scientific='Lasiodora parahybana',
  //   image='',
  //   acquired=[???],
  //   endemic='Brazil (forest)',
  // ),
  Spider(
    personal='Beans',
    common='Brazilian White Knee',
    scientific='Acanthoscurria geniculata',
    image='2023-04-04-beans.jpg',
    acquired=[10, 8, 2022],
    endemic='Northern Brazil',
  ),
  Spider(
    personal='Buzz Queen',
    common='Costa Rican Zebra',
    scientific='Aphonopelma seemani',
    image='2022-10-20-buzz.jpg',
    acquired=[1, 10, 2022],
    endemic='Costa Rica, Honduras, Nicaragua',
  ),
  Spider(
    personal='Blanca',
    common='Brazilian Red and White',
    scientific='Nhandu chromatus',
    image='2022-10-01-blanca.jpg',
    acquired=[1, 10, 2022],
    endemic='Brazil and Paraguay',
  ),
  Spider(
    personal='Tiny',
    common='Mexican Red Rump',
    scientific='Tlitocatl vagans',
    image='2024-05-21-tiny.jpg',
    acquired=[11, 3, 2023],
    endemic='Mexico and Central America',
  ),
  Spider(
    personal='Charlene',
    common='Arizona Blonde',
    scientific='Aphonopelma chalcodes',
    image='2023-12-27-charlene.jpg',
    acquired=[27, 12, 2023],
    endemic='Arizona and Mexico (deserts)',
  ),
  Spider(
    personal='Astuary Art',
    common='Jalisco Gold Top',
    scientific='Aphonopelma sp. Jalisco',
    image='2024-02-27-astuary-art.jpg',
    acquired=[27, 12, 2023],
    endemic='Mexico',
  ),
  Spider(
    personal='Jacob Leespider',
    common='Texas Brown',
    scientific='Aphonopelma hentzi',
    image='2024-07-14-jacobleespider.jpg',
    acquired=[14, 7, 2024],
    endemic='Colorado, Kansas, Missouri, New Mexico, Oklahoma, Arkansas, Texas, and Louisiana',
  ),
];

{
  'spiders.json': spiders,
}
