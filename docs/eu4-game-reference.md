# EU4 Game Mechanics Wiki Scrape

Source: EU4 Paradox Wiki (eu4.paradoxwikis.com)
Scraped: 2026-03-31

---

## Armies

This page deals with the recruitment and maintenance of armies. For specific combat mechanics see land warfare. For different individual unit types see land units. For Mercenaries and special units see Special land units.

An army refers to a country's land forces.

The basic unit of land forces is the regiment, each consisting of 1000 soldiers at full strength. Each regiment is classed as Infantry, Cavalry or Artillery. Regiments are grouped into armies. Each army can be led by a general or conquistador.

### Recruiting an army

Recruiting regular forces requires an owned, cored, unoccupied province to recruit in, and three resources: manpower, ducats, and time. Each province can recruit one regiment at a time, though multiple regiments can be queued up in a single province. Regiments can be recruited in several ways:

When multiple regiments are recruited at once, the construction will usually be spread over multiple provinces and the regiments will automatically move to the province where the construction was started and join together into one army.

The base cost and time of a regiment depends on its type; this is then adjusted by any modifiers, in particular any buildings the province might have. Regiments start with 50% of maximum morale.

### Manpower

It takes 1000 manpower to recruit a regiment. Manpower is also used for reinforcing depleted regiments.

### Regiment cost

Regiment cost = base cost × max(100% + Σ regiment cost modifiers, 20%)

#### Base cost

The base costs for recruiting a regiment are:
- Infantry: 10 ducats
- Cavalry: 25 ducats
- Artillery: 30 ducats

#### Regiment cost modifiers

Regiment cost may be affected by general and type-specific modifiers which are summed.

##### General modifiers

- −20% as Tengri country
- −5% for trading in iron
- −10% with parliament and "Expand the Army" as active issue
- −33% as optional difficulty bonus
- +1% for each percentage point of inflation

Ideas and policies:
- −10%: Quantity idea 3: Enforced Service, various national ideas (Chernihiv, Karelian, Kikuchi traditions; Armenian, Colonial, Polish ideas; Expansion-Defensive policy)
- −5%: Plutocratic idea 1: Tradition of Payment

##### Type-specific modifiers

**Infantry** - Ideas: Berg traditions, Mewari traditions (-20%), Ava traditions (-15%), Butua/Guarani/Jaunpuri/etc. traditions (-10%)

**Cavalry** - +20%/−20% from Cossacks estates, −20% from tribes estates, −10% from trading in livestock. Horde government idea 1: −33%, Aristocratic idea 3: −20%, various national ideas −10%/−15%

**Artillery** - Smolenskian idea 4: −20%, Rajputana idea 6: −15%, Russian idea 3: −10%

### Recruitment time

Recruitment time = base time × (100% + Σ recruitment time modifiers)

#### Base time
- 60 days for infantry
- 90 days for cavalry
- 120 days for artillery

#### Recruitment time modifiers

Countrywide:
- −20% for trading in copper
- −10% with parliament and "Expand the Army"
- +2% for each point of war exhaustion

Provincial:
- +20% for blockaded provinces
- +30% for looted provinces
- +10% for each point of local unrest
- −2% per provincial tax development

### Composition

To maximize combat effectiveness of an army, the ratio of infantry, cavalry and artillery is vital:
- To avoid the insufficient support penalty, an army must not surpass the maximum ratio of cavalry per infantry regiments.
- Artillery can fire from the second line, and therefore can vastly increase the effectiveness of an army.

---

## Navies

[Page returned 404 - empty wiki page. The correct page may be at /Navy or /Naval_warfare]

---

## Trade

Trade and production of trade goods are two of the three main sources of income for a country, the third being taxes. Every province produces trade goods, which give production income to their owner directly. The trade value of the goods then enters a system of trade nodes, where it is steered and eventually collected by merchants as trade income.

### Summary

- Trade nodes across the world are connected to form a global network of trade. Money flows between trade nodes in unidirectional trade routes and terminates at end nodes. These connections are fixed and cannot be altered.
- Trade value represents the monthly sum of locally produced and incoming trade goods in a trade node.
- Trade power is a number representing a country's control over trade in a node. Power is used either to retain trade value (collecting) or transfer it forward (steering).
- Merchants can be sent to a trade node to collect or steer trade value.

### Sources of trade value

**Local trade value** = Local goods produced × price of the trade good. Can be modified by trade value modifiers from events (e.g., Controls Tea Trade +20%, Diamond District +10%).

**Multiple merchant bonus** - Each merchant steering applies a boost to outgoing trade value:
- 1 merchant: +5.0%, 2: +7.5%, 3: +9.1%, 4: +10.3%, 5: +11.3%
- Modified by trade steering bonus

### Trade nodes and power

Each province belongs to exactly one trade node. Three end nodes: English Channel, Genoa, Venice. A handful of origin nodes (California, Lhasa, Great Lakes).

**Collecting trade** - Each country has a main trade city. Collecting outside main trade city: −50% trade power penalty (multiplicative). Can be reduced by various missions/monuments.

### Embargo

Embargoing reduces the target's trade power in shared nodes by a percentage equal to your trade power share, times your embargo efficiency.

---

## Warfare

Warfare is one of the primary ways to obtain territory and other concessions from other nations.

### Starting a war

Declaring war requires a diplomat. War may not be declared on an ally, subject, guaranteed nation without first breaking that relation.

### Casus belli

The aggressor picks a casus belli which determines the wargoal, peace deal options, and costs in warscore/aggressive expansion/diplo power.

### No casus belli

Declaring war without a CB: −20 aggressive expansion, −2 stability, +2 war exhaustion. Halved with full Diplomatic ideas.

### Good relations

Declaring war on a country with opinion >100: −1 stability, +1 war exhaustion. Opinion >150: −2 stability, +2 war exhaustion.

### Co-belligerence

If marked as co-belligerent: can call own allies, guarantor called, province costs equal war leader's provinces.

### Things you cannot do while at war

Cannot: abdicate ruler, seize estate lands, reduce autonomy, upgrade/downgrade CoTs, return/sell/buy provinces, release subjects, provoke revolts, sell ships, threaten war, annex vassals (without scutage), create/revoke march, intervene as great power, move capital, move main trade city.

### War leader

The war leader on attacking side is the declaring country; on defending side it's the target. War leader negotiates peace for all allies.

### Military and port access

All nations on same side have military access to each other's lands. Can dock at each other's ports.

### War exhaustion

Represents the will to fight. High war exhaustion saps armies' ability to fight and reinforce.

### Call for peace

If warscore is 66.6%+ and 5 years since war start, ticking war exhaustion begins at +0.005/month, increasing by +0.005 each month.

### Warscore

Scale: +100% (complete victory) to −100% (complete defeat). Measured by: occupied provinces, battles won/lost (max 40%), blockaded ports, met war goals (ticking up to 25%).

---

## Colonization

Nations can explore and colonize the Americas, Asia, Africa, Australia, Siberia and Pacific islands.

### Objectives

Colonialism improves income (trade) and military logistics. Create colonial nations (AI subjects) and trade companies (semi-autonomous provinces with trade bonuses).

### Prerequisites

- A colonist (from national ideas, idea groups, parliament, or religious reform)
- An empty province adjacent to core or within colonial range of a port
- Ducats for maintenance (rises quadratically if colonies exceed colonists)

### Discovery

- Conquistador needed for land exploration, explorer for sea exploration
- "Quest for the New World" (Exploration idea 1) required for explorers/conquistadors
- With El Dorado: automatic exploration missions available
- Share Maps and Steal Maps diplomatic actions

### Colonists

Gained from Exploration and Expansion idea groups, various national ideas. Colonist grows colony population over time.

### Colonial maintenance

Cost increases quadratically when number of colonies exceeds number of colonists.

---

## Government

Each country is ruled by a government of a specific type. Government forms range from constitutional republics to despotic monarchies.

### Government types

**Monarchy** - Power held by single individual (monarch). Uses legitimacy. Access to royal marriages and personal unions.

**Republic** - Power held by group. Uses republican tradition instead of legitimacy. Election cycle system.

**Theocracy** - Power held by religious elite. Designate heir from candidates. Uses devotion.

**Tribal government** - Society without developed nation-state concept. Uses legitimacy (or horde unity for steppe hordes).

**Native Tribe** - Government of native tribes in Americas/Australia. No legitimacy system.

### Switching government type

Monarchies, Republics, Theocracies can switch freely between each other. Tribes can become any but not vice versa. Native Tribes can reform into any other type.

### Government rank

Three ranks: Duchy (1), Kingdom (2), Empire (3).

| Rank | Required Dev | Diplomats | Governing Capacity | Max Absolutism | Autonomy Reduction |
|------|-------------|-----------|-------------------|----------------|-------------------|
| Duchy | Base | +0 | +0 | +0 | −0 |
| Kingdom | 300 | +1 | +200 | +0 | −0.025 |
| Empire | 1000 | +1 | +400 | +5 | −0.05 |

### Fixed government rank

Some government reforms have fixed rank (e.g., Celestial Empire = Empire, Shogunate = Kingdom, Daimyo = Duchy).

---

## Religion

The religion a nation follows affects gameplay significantly: benefits, mechanics, diplomacy, unrest.

### Religions and denominations

Major religions with DLC expansions:
- Wealth of Nations: Reformed, Hindu, Norse
- El Dorado: Inti, Mayan, Nahuatl
- The Cossacks: Tengri
- Mandate of Heaven: Confucian, Shinto
- Third Rome: Orthodox
- Cradle of Civilization: Sunni, Shia, Ibadi
- Rule Britannia: Anglican
- Emperor: Catholic, Hussite
- Leviathan: Alcheringa, Totemist, Zoroastrian, Sikh
- Origins: Jewish
- Base game: Protestant, Mahayana, Theravada, Vajrayana, Coptic, Fetishist

### Religious unity

Percentage of development from provinces following state religion or positively tolerated heretic/heathen religion.

Effects per percentage point:
- +0.01 monthly fervor, +0.05 max absolutism, +0.05% Clergy/Brahmins loyalty, +0.01 yearly harmony

Below 100%: +1% stability cost per point, +0.03 national unrest, −1% church power, +0.001 yearly corruption

### Tolerance

Three values: tolerance of the true faith (+3 base), tolerance of heretics (−2 base), tolerance of heathens (−3 base).

Each positive point: −1 local unrest. Each negative point: +1 local unrest.

True faith tolerance has no maximum. Base value +3.

---

## Absolutism

Absolutism represents how ruthless and efficient a government is. Unlocked from Age of Absolutism onwards. Gives scaling bonuses.

At 100 Absolutism:
- +5% Discipline
- +30% Administrative efficiency
- −50% Foreign core duration
- −50% Monthly decadence

### Yearly absolutism ideas

- +1.0: Cirebonese, Scandinavian, Swedish, Veronese ideas
- +0.5: Aristocratic idea 7, Portuguese idea 6, Siamese idea 6

### Changing absolutism

Increasing: +2 Strengthen government, +1 increasing stability, +1 decreasing autonomy (per 20 dev), +1 harsh treatment

Decreasing: −1 decreasing war exhaustion, −1 debasing currency, −2 increasing autonomy (per 20 dev), −10 accepting rebel demands

### Maximum absolutism

Base: +65. Republics: −40. Crown land: −50 to +15.

Government reforms modify max absolutism significantly (range: −50 to +50).

---

## Legitimacy (Monarchy)

Monarchy is a form of government where power is held by a single individual (the monarch). The ruler reigns until death. Royal marriages and personal unions are mostly limited to monarchies.

Monarchies have access to Aristocratic idea group (unless changed by government reform).

### Legitimacy

Legitimacy measures how valid a dynasty's claim to the throne is. Range 0-100.

Base: 0 (usurper) to 100 (established dynasty).

Effects of legitimacy:
- At 100: −2 national unrest, +1 diplomat, +0.5 yearly prestige
- At 0: +2 national unrest, −1 diplomat, −1 yearly prestige, +50% stability cost

### Reform tiers

Monarchies have 11 government reform tiers covering Power Structure, Noble privileges, Bureaucracy, State and Religion, Military Doctrines, Deliberative Assembly, Administrative Cadre, Economic Matters, Legitimation of Power, Absolutism & Constitutionalism, Separation of Power.

---

## Subject nations

Subject nations are semi-autonomous subordinate nations that surrender economic/diplomatic/military power to their overlord.

### Subject types

**Vassal** - Basic subject. Auto-joins overlord's wars. Pays subject tax (1 × income_from_vassals × their tax income). Overlord gets +10% of subject's land force limit. Can be integrated after 10 years. Liberty desire per dev: 0.25.

**March** - Militaristic vassal. Cannot be annexed, no taxes. Gets +30% land/naval force limit, +25% national manpower, +20% manpower recovery, +20% fort defense, −20% fort/land/naval maintenance (if dev ≤ 25% of overlord). Base liberty desire: −15%.

**Client state** - Custom vassal with permanent −25% liberty desire. Unlocked at diplo tech 23.

**Daimyo** - Unique vassalage to Japan's shogun. Can fight other daimyo. Base liberty desire: +10%.

**Incorporated vassal** - Traditional vassal but costs governing capacity for −25% diplomatic annexation cost.

**Colonial nation** - Formed in colonial regions. Provides trade power, tariffs, and can fight in colonial wars. 10 provinces triggers formation.

**Trade company** - Semi-autonomous provinces. +100% trade power, ignore religious differences. Cannot form in Europe (without special cases).

**Tributary** - Pays annual tribute (monarch points or percentage of income). Can be called to war but not forced.

---

## Development

Development is a province attribute with three kinds: base tax (admin), production (diplo), manpower (military).

### Effects of development

Per development level:
- **Base tax**: −2% local recruitment time, +1 yearly tax income base, +2% institution spread
- **Production**: trade value, production income
- **Manpower**: +250 maximum manpower, +1% garrison growth

Per point of development (any category):
- +0.1 possible buildings
- +2% supply limit modifier
- −0.1% local missionary strength
- +0.1 land force limit
- +0.1 naval force limit
- +60 sailors (coastal)
- +0.2 local trade power

### Development cost formula

Final cost = 50 × (1 + Dev Cost Modifier + Local Dev Cost Modifier) × Max(0.1, 1 + Dev Cost + Local Dev Cost)

Cost increases: +3% per point above 9 dev, +3% per point above 19, +3% per point above 29, etc.

Minimum cost can reach 0 (floored, not negative).

---

## Combat

[Redirected to Warfare page - same content as Warfare section above]

---

## Province

Provinces are the smallest division in EU4. 3272 land provinces total. They provide income, manpower, trade goods.

### Terms and mechanics

**Development** - Measure of province wealth/productivity. Divided into base tax, production, manpower.

**Tax** - Each province has base tax. Can be improved with admin points.

**Production** - Each province produces a trade good. Can be improved with diplo points.

**Manpower** - Each province contributes to national manpower pool. Can be improved with military points.

**Defence** - Forts exert zone of control. Must be taken before enemy armies pass through.

**Trade** - Each province produces trade power and contributes trade value.

**Autonomy** - Degree of government control. Lower = more productive. 100% autonomy = no tax/manpower/trade power.

**Unrest** - Chance of rebellion. Lowered by increasing autonomy.

**Devastation** - From sieges/occupation/scorched earth. At 100%: −200% goods produced, −50% supply limit, −200% institution spread, +20% dev cost.

**Cores and claims** - Cores represent rightful territory. Claims through espionage or disputes.

**Culture and religion** - Foreign cultures/non-state religion = more rebellious and less productive.

**Buildings** - Number of building slots based on development level.

**Capital** - Political center. Costs 200 admin to move (base).

**Main trading port** - Trade auto-collected here. Can be moved for 200 diplo power.

---

## Military leader

Military leaders come in two types: land (generals/conquistadors) and naval (admirals/explorers).

- Conquistadors/explorers need "Quest for the New World" (Exploration idea 1)
- Male monarch/heir can become leader (no cost, slightly higher death chance)
- Leader skill depends on army/navy tradition at hiring
- Most leaders last ~12 years before dying
- Drilling may increase pips; winning battles may award special traits

### Recruiting cost

Base cost: 50 monarch points (military for land, diplomatic for naval).

Modifiers:
- −50% at 100% army professionalism (generals)
- −25% Maritime idea 6 (admirals)
- −10% Aristocratic idea 5, Divine idea 3

### Abilities (0-6 scale)

**Fire** - Added to dice roll during fire phase.

**Shock** - Added to dice roll during shock phase.

**Maneuver** - Affects movement speed (+5% per pip, max 30%). Reduces supply weight. Negates river/strait crossing if +1 more than defender. +10% reinforce speed in unowned terrain per pip.

**Siege** - Land: +1 to siege roll per pip. Naval: +10% blockade effectiveness per pip.

Ideas improving leader abilities:
- Land leader fire +1: Offensive idea 3, Great Ming idea 7, Rajput idea 6
- Land leader shock +1: Manchu/Scottish/Timurid traditions, Offensive idea 1, many national ideas

---

## Rebels

Rebellions rise up when subject peoples are angered. Primarily caused by unrest.

### Unrest

Each province has unrest number. Sum of local unrest + national unrest.

**National unrest factors**: stability, war exhaustion, overextension, advisors, ideas.

**Local unrest factors**: culture, religion, separatism, autonomy.

Ideas reducing unrest:
- −2: Divine idea 6, Humanist idea 1, many national ideas
- −1: Many traditions and national ideas

### Reducing unrest

- Local autonomy: +10% = −10 unrest for 30 years
- Stability, war exhaustion reduction, Theologian advisor, troops, culture conversion, religion conversion

### Separatism

Newly conquered non-core province gets 30 years of separatism = +15 base unrest (0.5/year decay).

Reduced by ideas (−5 years of separatism from various sources), reconquest CB.

---

## National ideas

National ideas are country-specific bonuses unlocked by completing idea slots. Each country has 7 national ideas plus traditions and ambitions.

National ideas are distinct from idea groups. They are tied to the country tag and provide historically-themed bonuses.

### Structure

- **Traditions**: 2 bonuses active from game start
- **National Ideas**: 7 bonuses unlocked as admin tech levels increase (one per idea group slot)
- **Ambition**: 1 bonus unlocked when all 7 national ideas are completed

National ideas can be swapped when forming new nations. Some nations share idea sets (see Group national ideas).

Countries form through decisions and missions, often swapping their national ideas for new ones.

---

## Policies

Policies are bonuses unlocked by completing idea groups. Each pair of idea groups from different types (admin-diplo, admin-mil, diplo-mil) unlocks a policy.

There are 7 admin × 7 diplo + 7 admin × 11 mil + 7 diplo × 11 mil = 203 possible policies.

### Rules

- Up to 8 idea groups per nation → up to 21 possible policies
- Maximum 3 active policies per monarch point type (3 admin, 3 diplo, 3 military)
- First policy of each type is free; subsequent cost 1 monarch point/month
- Once activated, cannot deactivate for 10 years

### Additional policy slots

- +1 possible policies: Holy Roman traditions, Scandinavian idea 2, Sicilian idea 2, Swedish idea 1
- +1 admin: Legislative Houses (T7 monarchy), Political Principle (T7 republic)
- +1 diplo: Court idea 7, Spanish idea 7
- +1 military: Barbary Corsair idea 7, Cossack idea 7

### Free policies

- +1 free: Autonomous Swiss Cantons (T1 republic/theocracy), Two-Chamber System (T5 monarchy/T6 republic), Church and State (T7 theocracy), Innovative idea 7

---

## Estates

Estates are factions within the nation influencing domestic politics. They have influence and loyalty attributes, apply national modifiers, and can grant privileges.

### Estates available

Most nations have 3 base estates: Burghers, Clergy, Nobility.

Additional estates based on context:
- Cossacks (Eastern tech Christian + steppe terrain)
- Dhimmi (Muslim nations)
- Tribes (nomadic tribes - replaces all others)
- Brahmins (Hindu nations)
- Jains/Vaishyas (Indian tech)
- Marathas/Rajputs (Indian tech, specific cultures)
- Janissaries (Ottomans)
- Eunuchs (Emperor of China)
- Qizilbash (Ardabil/Persia)

### Estate mechanics

**Loyalty** (0-100): Disloyal (0-29), Neutral (30-59), Loyal (60-100). Trends toward equilibrium.

**Influence** (0-100): Determines strength of estate effects. Levels: 0-19/20-39/40-59/60-100 (×0.25/0.50/0.75/1.0).

**Privileges**: Grant bonuses but reduce max absolutism.

### Crownland

Land divided among estates and crown. Crownland bonuses scale from 0% to 100%:
- 0-4%: −40 max absolutism, +0.30 autonomy, −20% tax, +100% liberty desire
- 30-49%: neutral
- 100%: +15 max absolutism, −0.05 autonomy, +100% reform progress

**Seize Land**: Available every 5 years (not at war). +5% crownland, all estates lose 20% loyalty. Rebels spawn if any estate drops below 30% loyalty.

---

## Technology

Three technology types: Administrative, Diplomatic, Military. Each has 33 levels.

### Types

**Administrative** - Government types, production efficiency, national idea slots, buildings (stability/income), administrative efficiency, formable nation requirements (tech 10).

**Diplomatic** - Trade efficiency, colonization range, diplomatic influence, naval power, trade/sea buildings.

**Military** - Land forces improvement, troop types, morale, maneuver, tactics, warfare buildings.

### Technology groups

Starting levels and institution penalties:
- Western/Eastern/Anatolian/Muslim/Indian/Chinese/East African: tech 3, +0%
- West African/Central African/Nomadic/Polynesian: tech 2, +50%
- Mesoamerican/Andean/North American/South American/Aboriginal: tech 1, +50%

### Cost formula

Technology cost = base cost × (100% + general tech cost modifiers + institution penalty)

Base cost: 600 monarch points per level.

### Key modifiers

- **Institution penalty**: +15%/+30%/+50% per unembraced institution (accumulates, max +400%)
- **Neighbor bonus**: −5% per level behind most advanced neighbor (max −75%)
- **Technology cost increases over time**: 0% at 1444 to +30% at 1821 (linear based on historic discovery date)

---

## Manpower

Manpower is a country's stock of men eligible for military service. Used to recruit and reinforce armies (except mercenaries).

### Maximum manpower

Base value: +10,000 men.

Additional sources:
- +500 as HRE emperor per member state
- +1,000 as HRE emperor per free city
- +5,000 with Municipal Self-Defense (T5 republic reform)
- +2,000 per Governor General's Mansion trade company investment

### Province manpower formula

Province manpower = (base + local manpower increase) × (1 + local manpower modifier + national manpower modifier) × (1 − local autonomy)

#### Base manpower

Each level of military development = 250 men.

#### Local manpower modifiers

- +100% Training Fields
- +75% Core province
- +50% Barracks
- +33% Patriarch authority 100% (Orthodox)
- +25% Land province (base)
- −15% Non-accepted culture in primary culture group
- −33% Non-accepted culture outside primary culture group
- −50% Occupation
- −1% per point of autonomy (multiplicative)

#### National manpower modifier

- +50% with difficulty set to 'very easy'
- +30% with Crusade triggered modifier
- +25% as march
- +20% with Tsardom government reform
- Various national ideas and policies

### Manpower recovery

Base recovery: 10,000 × (1 + national manpower modifier) per year.
Recovery rate can be increased by ideas, buildings, and policies.

Ideas increasing national manpower:
- +15%/+10%: Many national ideas (Polish, Hungarian, Ottoman, etc.)
- +20%/+15%: Various idea groups (Quantity gives +50% national manpower)
