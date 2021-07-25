## Guidelines for contributing

Lol, just contribute. Make a pull request or some issues, I'm pretty lonely right now.

## How to contribute
To contribute, submit a pull request at [https://github.com/SSS-Says-Snek/name_goes_here_lol/pulls](https://github.com/SSS-Says-Snek/name_goes_here_lol/pulls).
Major changes such as implementing a new currency in the shop would be reviewed by me,
while small changes like balancing items and buffs will... still be reviewed by me.
When contributing, there are certain rules to follow, listed down below

## Requirements for contributing
- [X] Contributions must solve a problem and/or fix a bug
- [X] Contributors are expected to follow the project's Code of Conduct
- [X] Contributors must not add harmful contributions to the project
- [X] Contributors are expected to follow [PEP 8](https://python.org/dev/peps/pep-0008)
- [X] Major contributions (E.g new game feature) must be approved by SSS-Says-Snek first before merging to the project
- [ ] Contributors should be as rude and mean to each other as possible

## Your guide to contributing to name_goes_here_lol

There are a few things to know before you start contributing to the game
1. First of all, contributors are advised and expected to follow PEP 8, to create clean code. If you do not comply to PEP 8, 
  there is less of a chance that your PR would not be merged
2. It is strongly advised for contributors to add comments and docstrings to their code. However, if they do not add comments/docstrings, 
  it doesn't really matter, as long as their code is somewhat readable
3. There are a couple misleading function names in the project. For example, `handle_events()` actually only handles one event.
  Be careful with the function names!
4. Try to avoid files that are larger than 3,000 lines of code, as the code starts to get less readable. ***HOWEVER***, the main 
  exception to this rule is `state.py`, as it would cause a circular import if the file is split
5. As a continuation to rule number 1, ***please, please, PLEASE*** DO __NOT__ write messy code. It would:
   A: Cause confusion about the code
   B: Cause future contributors to not be able to contribute to that piece of code
   
## How to get your Pull Request merged 🌟

When you wrap up your contributions to the game, how do you implement it in the game? Well, that's where __pull requests__ come in.
If you didn't already know (you SHOULD know it already), pull requests are an easy way to get your contributions merged to the game in GitHub.

There is a special system (a hierarchy, maybe?) to merging a pull request on this game. Please review the following **CAREFULLY**:

### Ideal System (Hierarchy?)
There are 3 hierarchies in this system: Lead Developer, Core Dev Team, and Dev Team.

#### Article I: Different hierarchies and their roles
1. **Dev Team** (DT): Once a person contributes to the project in ANY way, they are automatically promoted to a Dev Team member.
However, there can be overrulings, as explained in Article ***TODO***. A contribution can be fixing a typo, or making GTA V into the game :kekw:
2. **Core Dev Team** (CDT): Once a person contributes enough ("Enough" will be heavily decided on the quality of their contributions, not the quantity),
The Lead Developer and other Core Dev Team members will get the chance to promote them. The Core Dev Team, while not being as important to the game
as say, the Lead Developer, they are essential to the game, and also have a lot of power
3. **__Lead Developer__** (LD): The lead developer is the person overseeing the entire project: Game, Dev Team, you name it.
The lead developer gets **a lot** of the say in what is to be added to the game.   

#### Article II: Ways to be promoted into the hierarchies
We have established that there are 3 types of roles: `Lead Developer`, `Core Dev Team`, and `Dev Team`. 
This section goes further into detail on how to obtain these roles, and how to be promoted to a higher role.

1. **PROMOTION TO A DEV TEAM MEMBER:** As said in Article I, Section III, team members will automatically be promoted to a DT once they contribute 
to the game __in any way__. However, there can be overrulings of this decision:
   - To start an overruling, there must be at least 1/3 of the `Core Dev Team` that is willing to overrule
   - Once the decision to overrule is finalized, the overruling trial begins: the `Dev Team` and the `Core Dev Team` vote on if the overruling 
    is valid or not. If the overruling reaches a 3/4 majority, then the person will not become a Dev Team Member. 
   - ***HOWEVER***, the Lead Developer
    can __veto__ the decision. Once the Lead Developer vetoes, the only way to unveto is to reach another 2/3 majority.
2. **PROMOTION TO A CORE DEV TEAM MEMBER**: As said in Article I, Section II, when a `Dev Team` member contributes enough, 
a vote will be held to decide whether they should be promoted. As usual, there are a couple rules to this:
   - "Enough" contributions is decided more so on the contributor's quality of commits, rather than the quantity of commits. **HOWEVER**, note that 
    the amount of contributions is also considered. Generally, to become a CDT member, you must have at least 100 line changes.
   - To be promoted to a CDT member, the existing `Core Dev Team` and the `Lead Developer` vote on whether they should be promoted. 
    There needs to be a 2/3 majority for promotion in order to be promoted.
   - As usual, the Lead Developer gets the power to veto any decision. Once the Lead Developer vetoes a decision, the Core Dev Team can 
    **veto the veto**, with a 3/4 majority.
3. **PROMOTION TO A LEAD DEVELOPER**: As the lead developer is the __only__ role with one person, it is hard to be promoted to a Lead Developer. 
However, there is one way to get promoted, but it must satisfy the followign conditions:
   - The Lead Developer has been inactive for more than 6 months
   - The `Dev Team` and the `Core Dev Team` had a 90% majority
   - Someone is *willing* to become a Lead Developer
Only **THEN**, can a vote of the new Lead Developer start. All the contributors who want to be Lead Developer will be candidates, and all people from 
the `Dev Team` and the `Core Dev Team` will be allowed one vote, __REGARDLESS OF RANK__. Whoever gets the most votes becomes Lead Developer.