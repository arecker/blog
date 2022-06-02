local ArchiveRedirect(source='', target='', status='301!') = (
  local baseUrl = 'https://archive.alexrecker.com';

  assert source != '' : 'source required';

  local t = if target != '' then target else source;
  [source, baseUrl + t + ' ' + status]
);

[
  ArchiveRedirect(source='/our-new-sid-meiers-civilization-inspired-budget/', target='/civ-budget.html'),
  ArchiveRedirect(source='/seinfeld.html'),
  ArchiveRedirect(source='/anxiety.html'),
  ArchiveRedirect(source='/clockwork-orange.html'),
  ArchiveRedirect(source='/eyes-wide-shut.html'),
  ArchiveRedirect(source='/full-metal-jacket.html'),
  ArchiveRedirect(source='/jane.html'),
  ArchiveRedirect(source='/linux.html'),
  ArchiveRedirect(source='/noah.html'),
  ArchiveRedirect(source='/rockford.html'),
  ArchiveRedirect(source='/san-francisco.html'),
  ArchiveRedirect(source='/the-top-5-ways-that-my-corgi-has-taught-me-how-to-be-a-better-person.html'),
  ArchiveRedirect(source='/uhh-yeah-dude.html'),
  ArchiveRedirect(source='/using-selenium-buy-bus-pass/', target='/selenium-bus-pass.html'),
]
