local Pet(name, category, image) = {
  name: name,
  category: category,
  image: image,
};

local Dog(name, image) = Pet(name, 'Dogs', image) {
  species: 'Canis lupus familiaris',
};

local dogs = [
  Dog('Ollie', 'pets-ollie.jpg') {
    breed: 'Pembroke Welsh Corgi',
    birthplace: 'Elizabeth, Illinois',
    gotcha: 'May 25, 2014',
    aliases: 'Crig, The Big Cheese, The Queso-Man, Cheese-a-Rone',
    likes: 'Panera Cheese Souffles, comedy, meaningful relationships',
    dislikes: 'Invading his personal bubble',
  },

  Dog('Ziggy', 'pets-ziggie.jpg') {
    breed: 'Cardigan Welsh Corgi',
    birthplace: 'Philadelphia, Pennsylvania',
    gotcha: 'October 11, 2017',
    aliases: 'Peanut, Peen-peen, Suh-peena, The Mosasaurus',
    likes: 'Agility, Walks with dad, Special treatment',
    dislikes: 'Being ignored, dogs on the TV, things that suddenly get really big',
  },

  Dog('Minnie', 'pets-minnie.jpg') {
    breed: 'Cardigan Welsh Corgi',
    birthplace: 'Lewisberry, Pennsylvania',
    gotcha: 'April 10, 2021',
    aliases: 'Iron Minnie, Minnistrone, Dylan "Strone", Minniestrouneliotis',
    likes: 'Being super smart, things that crunch, her big brother',
    dislikes: 'Guilty feelings',
  },
];

local Fish(name, image) = Pet(name, 'Fish', image);

local fish = [
  Fish('Ibb', 'pets-ibb.jpg') {
    species: 'Amphiprioninae',
    commonName: 'Clown Fish',
    gotcha: 'September 24, 2020',
    aliases: 'The one without the dots',
    likes: 'Food, Clean water, Finding Nemo',
    dislikes: 'Obb',
  },
  Fish('Obb', 'pets-obb.jpg') {
    species: 'Amphiprioninae',
    commonName: 'Clown Fish',
    gotcha: 'September 24, 2020',
    aliases: 'The one with the dots',
    likes: 'Anemones, food, imposing her will',
    dislikes: 'Death (especially anemones)',
  },
];

local Reptile(name, image) = Pet(name, 'Reptiles', image);

local reptiles = [
  Reptile('Ducky', 'pets-ducky.jpg') {
    species: 'Eublepharis macularius',
    commonName: 'Leopard Gecko',
    gotcha: 'October 21, 2021',
    aliases: 'Duckasaurus, Duckanator',
    likes: 'Naps, mealworms, warm surfaces',
    dislikes: 'Superworms, head scratches, hard work',
  },
];

local Spider(name, image) = Pet(name, 'Spiders', image);

local spiders = [
  Spider('Spidey', 'pets-spidey.jpg') {
    species: 'Tlitocatl verdezi',
    common: 'Mexican Rose Grey Tarantula',
    gotcha: 'July 5, 2021',
    likes: 'His favorite rock',
    dislikes: 'New things',
  },
  Spider('Karta', 'pets-karta.jpg') {
    species: 'Brachypelma hamorii',
    common: 'Mexican Redknee Tarantula',
    gotcha: 'July 5, 2021',
    likes: 'Alone time, roaches',
    dislikes: 'Wet dirt, noises, silliness',
  },
  Spider('Glassy', 'pets-glassy.jpg') {
    species: 'Tliltocatl albopilosus',
    common: 'Curly Hair Tarantula',
    gotcha: 'July 16, 2021',
    likes: 'Digging, Spending alone time in his hidey-hole',
    dislikes: 'Tapping on his glass',
  },
  Spider('Venom', 'pets-venom.jpg') {
    species: 'Grammastola pulchra',
    common: 'Brazilian Black Tarantula',
    gotcha: 'October 6, 2021',
    likes: 'Throwing dirt, drinking water',
    dislikes: 'Feeling hungry',
  },
  Spider('Leo', 'pets-leo.jpg') {
    species: 'Chromatopelma cyaneopubescens',
    common: 'Greenbottle Blue Tarantula',
    gotcha: 'October 6, 2021',
    likes: 'Dancing, making webs, murdering defenseless insects',
    dislikes: 'Humid summers',
  },
  Spider('Spiker', 'pets-spiker.jpg') {
    species: 'Grammostola pulchripes',
    common: 'Chaco Golden Knee Tarantula',
    gotcha: 'October 6, 2021',
    likes: 'His house, darkness, super worms',
    dislikes: 'Being seen',
  },
  Spider('Tex', 'pets-tex.jpg') {
    species: 'Aphonopelma hentzi',
    common: 'Texas Brown Tarantula',
    gotcha: 'January 5, 2022',
    likes: 'Digging, killing baby roaches, James Taylor',
    dislikes: 'Sitting still',
  },
  Spider('Tio', 'pets-tio.jpg') {
    species: 'Davus pentaloris',
    common: 'Guatemalan Tiger Rump Tarantula',
    gotcha: 'January 14, 2022',
    likes: 'Gardening, meditation, shaking his butt',
    dislikes: 'The cold',
  },
];

local pets = dogs + fish + reptiles + spiders;

{
  'data/nav.json': ['entries.html', 'pets.html', 'contact.html'],
  'data/pets.json': pets,
}
