local Quote(author='', text='') = (
  assert author != '' : 'quote author required';
  assert text != '' : 'quote text required';

  {
    author: author,
    text: text,
  }
);

local quotes = [
  Quote(author='Mark Twain', text='Sanity and happiness are an impossible combination.'),
  Quote(author='Thomas Fuller', text='Trust thyself only, and another shall not betray thee.'),
  Quote(author='Mahatma Ghandi', text='Fear has its uses but cowardice has none.'),
  Quote(author='George Orwell', text='Happiness can exist only in acceptance.'),
  Quote(author='Steven H. Coogler', text='Seek respect mainly from thyself, for it comes first from within.'),
  Quote(author='Proverb', text="Conscience is the dog that can't bite, but never stops barking."),
  Quote(author='Steven H. Coogler', text='In general, pride is at the bottom of all great mistakes.'),
  Quote(author='Emily Dickinson', text='Anger as soon as fed is dead -- tis starving makes it fat.'),
  Quote(author='Anne McCaffrey', text='Make no judgements where you have no compassion.'),
  Quote(author='Carlos Salinas de Gortari', text='Isolation is a self-defeating dream.'),
  Quote(author='George C. Lichtenberg', text='Doubt must be no more than vigilance, otherwise it can become dangerous.'),
  Quote(author='Michael Novak', text='Love is a willingless to sacrifice.'),
  Quote(author='Richard R. Grant', text='The value of identity is that so often with it comes purpose.'),
  Quote(author='Thomas Edison', text='Discontent is the first necessity of progress.'),
  Quote(author='Herman Hesse', text='Some of us think holding on makes us strong, but sometimes it is letting go.'),
  Quote(author='Ralph Waldo Emerson', text='Let not a man guard his dignity but let his dignity guard him.'),
  Quote(author='Erma Bombeck', text='Guilt: the gift that keeps on giving.'),
  Quote(author='Ram Dass', text='Be here now.'),
  Quote(author='Lao Tzu', text='The master understands that the universe is forever out of control.'),
  Quote(author='James A. Lee Iacocca', text='Our biggest problems arise from the avoidance of smaller ones.'),
  Quote(author='Mother Teresa', text='Honesty and transparency make you vulnerable.  Be honest and transparent anyway.'),
  Quote(author='Edward Hodnett', text='If you do not ask the right questions, you do not get the right answers.'),
  Quote(author='Malachy McCourt', text='Resentment is like taking poison and waiting for the other person to die.'),
  Quote(author='John Churton Collins', text="If we knew each other's  secrets, what comfort should we find."),
  Quote(author='David Levithan', text='The mistake is thinking that there can be an antidote to the uncertainty.'),
  Quote(author='Hippocrates', text='Cure sometimes, treat often, comfort always.'),
  Quote(author='Robert Burns', text='Suspicion is a heavy armor and with its weight it impedes more than it protects.'),
  Quote(author='Eiji Yoshikawa', text='Sincerity, even if it speaks with a stutter, will sound eloquent when inspired.'),
  Quote(author='A.J. Jacobs', text='I have little shame, no dignity - all in the name of a better cause.'),
  Quote(author='Vanna Bonta', text='Truth may sometimes hurt, but delusion harms.'),
  Quote(author='Henri Poincare', text='Intuition is more important to discovery than logic.'),
  Quote(author='Suzanne Vega', text='How weird was it to drive streets I knew so well. What a different perspective.'),
  Quote(author='Christopher Hitchens', text='There can be no progress without head-on confrontation.'),
  Quote(author='Edward Albea', text="Sometimes it's necessary to go a long distance out of the way to come back a short distance correctly."),
  Quote(author='Leonard Sweet', text="Stagnation is death. If you don't change, you die. It's that simple. It's that scary."),
  Quote(author='John Green', text='In my opinion, actual heroism, like actual love, is a messy, painful, vulnerable business.'),
  Quote(author='Arthur Miller', text='Maybe all one can do is hope to end up with the right regrets.'),
  Quote(author='Aldous Huxley', text='If you have behaved badly, repent, make what amends you can and address yourself to the task of behaving better next time.'),
  Quote(author='Robert Louis Stevenson', text='Sooner or later everyone sits down to a banquet of consequences.'),
  Quote(author='G.K. Chesterton', text='We are all in the same boat, in a stormy sea, and we owe each other a terrible loyalty.'),
  Quote(author='Jeffrey Fry', text='In our quest for the answers of life we tend to make order out of chaos, and chaos out of order.'),
  Quote(author='Franklin D. Roosevelt', text='There are many ways of going forward, but only one way of standing still.'),
  Quote(author='Bruce Lee', text='Truth is outside of all patterns.'),
  Quote(author='Franz Kafka', text='By imposing too great a responsibility, or rather, all responsibility, on yourself, you crush yourself.'),
  Quote(author='Benjamin Franklin', text='How few there are who have courage enough to own their faults, or resolution enough to mend them.'),
  Quote(author='Doctor Who', text='Resistance is useless.'),
  Quote(author='Leo Tolstoy', text='Happiness does not depend on outward things, but on the way we see them.'),
  Quote(author='Lyndon Johnson', text="Being president is like being a jackass in a hailstorm.  There's nothing to do but to stand there and take it."),
  Quote(author='Albert Camus', text='In the depth of winter, I finally learned that within me, there lay, an invincible summer.'),
  Quote(author='African Proverb', text='If you refuse to be made straight when you are green, you will not be made straight when you are dry.'),
  Quote(author='Exodus 14:14', text='The Lᴏʀᴅ will fight for you while you keep silent.'),
  Quote(author='Kahlil Gibran', text="For in the dew of little things the heart finds it's morning and is refreshed."),
];


[[q.author, q.text] for q in std.sort(quotes, keyF=function(q) q.author)]
