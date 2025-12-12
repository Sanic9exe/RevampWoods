"""World builder - creates all game locations."""

from typing import Dict, List, Optional, Tuple, Any
import random

from .location import Location
from .models import Route
from .item_factory import ItemFactory
from .creature_factory import CreatureFactory
from .colors import Colors
from .utils import SkillType

# ============================================================================
# WORLD BUILDER - CREATES ALL LOCATIONS WITH NUMBERED ROUTES
# ============================================================================

class WorldBuilder:
    """Builds the game world with all locations and numbered routes."""
    
    @staticmethod
    def create_world() -> Dict[str, Location]:
        """Create all game locations with numbered route navigation."""
        locations = {}
        
        # ===================================================================
        # STARTING AREA - THE CLEARING
        # ===================================================================
        locations["clearing"] = Location(
            location_id="clearing",
            name="Forest Clearing",
            description="A small clearing in the dense forest. Sunlight filters through the canopy above.",
            long_description="""You stand in a small clearing surrounded by towering ancient trees. The air is thick 
with the scent of pine and damp earth. Sunlight filters through gaps in the canopy, 
creating dancing patterns on the forest floor covered in soft moss and fallen leaves.

You have no memory of how you got here, only a desperate urge to find your way out 
of this mysterious forest. The trees seem to watch you with ancient, unknowable eyes.

Several paths lead away from this clearing into the shadows of the forest.""",
            routes=[
                Route(1, "dark_woods", "A worn path leading into darker woods", danger_level=1),
                Route(2, "stream", "Follow the sound of running water to the east", danger_level=0),
                Route(3, "thorny_thicket", "Push through the thorny bushes to the south", danger_level=2),
                Route(4, "dense_forest", "A barely visible trail into the dense western forest", danger_level=1),
                Route(5, "old_oak", "Climb the massive old oak tree in the center", 
                      requires_skill=(SkillType.CLIMBING, 2), danger_level=1),
            ],
            items=[ItemFactory.create_item("rusty knife"), ItemFactory.create_item("healing herb"),
                   ItemFactory.create_item("torch")],
            features=["fallen log", "wildflowers", "old campfire remains", "mushroom patches"],
            ambient_sounds=["birds chirping", "leaves rustling", "distant woodpecker"],
            save_point=True,
            rest_allowed=True
        )
        
        # ===================================================================
        # OLD OAK TREE
        # ===================================================================
        locations["old_oak"] = Location(
            location_id="old_oak",
            name="Ancient Oak Tree",
            description="High in the branches of an enormous oak tree.",
            long_description="""You've climbed high into the branches of the ancient oak. From here, 
you can see far across the forest canopy - an endless sea of green stretching 
in every direction.

To the north, you spot a stone tower rising above the trees in the distance.
To the east, a river glitters like silver through the trees.
To the west, mountains loom on the horizon.
Something glints in a hollow in the trunk nearby.""",
            routes=[
                Route(1, "clearing", "Climb back down to the clearing", danger_level=0),
                Route(2, "squirrel_nest", "Investigate the hollow in the trunk", danger_level=0),
            ],
            items=[ItemFactory.create_item("feather"), ItemFactory.create_item("feather")],
            features=["panoramic view", "bird nests", "hollow in trunk", "thick branches"],
            ambient_sounds=["wind in leaves", "bird songs", "creaking branches"],
            climbable=True
        )
        
        locations["squirrel_nest"] = Location(
            location_id="squirrel_nest",
            name="Hollow in the Oak",
            description="A cozy hollow inside the ancient oak tree.",
            long_description="""The hollow is surprisingly spacious inside. It looks like squirrels 
have been using it as a storehouse - you can see nuts and acorns piled up.

But among the nuts, something else catches your eye...""",
            routes=[
                Route(1, "old_oak", "Return to the branches outside", danger_level=0),
            ],
            items=[ItemFactory.create_item("map fragment"), ItemFactory.create_item("wild berries")],
            creatures=[CreatureFactory.create_creature("squirrel")],
            features=["acorn pile", "soft bedding", "chew marks"],
            ambient_sounds=["scratching sounds", "chittering"]
        )
        
        # ===================================================================
        # STREAM AREA
        # ===================================================================
        locations["stream"] = Location(
            location_id="stream",
            name="Babbling Stream",
            description="A clear stream flows through the forest, its waters sparkling in the light.",
            long_description="""A crystal-clear stream winds its way through the forest, cutting a gentle 
path through moss-covered banks. The water looks clean and inviting, and you can 
see small silver fish darting beneath the surface. Smooth stones line the streambed, 
and ferns grow thick along the water's edge.

The stream seems to come from the north, where you can hear the distant roar of 
a waterfall. It flows east into a misty area where the forest becomes shrouded 
in perpetual fog.""",
            routes=[
                Route(1, "clearing", "Follow the path back to the clearing", danger_level=0),
                Route(2, "waterfall", "Follow the stream north toward the waterfall sound", danger_level=1),
                Route(3, "misty_grove", "Follow the stream east into the mist", danger_level=2),
                Route(4, "stream_south", "Cross the stepping stones to the south bank", danger_level=1),
                Route(5, "fishing_spot", "Find a good spot to fish", danger_level=0),
            ],
            items=[ItemFactory.create_item("fishing rod"), ItemFactory.create_item("fresh water")],
            features=["clear water", "smooth stones", "fish swimming", "ferns", "stepping stones"],
            water=True,
            ambient_sounds=["water bubbling", "frogs croaking", "stream flowing"],
            rest_allowed=True
        )
        
        locations["fishing_spot"] = Location(
            location_id="fishing_spot",
            name="Quiet Fishing Spot",
            description="A peaceful spot by the stream, perfect for fishing.",
            long_description="""You've found a quiet bend in the stream where the water pools 
into a calm, deep section. Fish gather here, making it an ideal fishing spot.

An old log provides a comfortable seat, and someone has even left a 
crude fish trap in the water.""",
            routes=[
                Route(1, "stream", "Return to the main stream area", danger_level=0),
            ],
            items=[ItemFactory.create_item("cooked fish")],
            features=["deep pool", "comfortable log seat", "fish trap"],
            water=True,
            ambient_sounds=["gentle lapping", "fish splashing"],
            special_actions=["fish"],
            rest_allowed=True
        )
        
        locations["stream_south"] = Location(
            location_id="stream_south",
            name="Southern Stream Bank",
            description="The southern bank of the stream, where the water flows faster.",
            long_description="""The stream flows more swiftly here, cutting deeper into the earth. 
The banks are higher, and you can see the water has exposed some rocky 
outcroppings. Something glints in the mud near the water's edge.

Animal tracks lead south into thick underbrush - it looks like a well-used 
game trail. The stream curves east around a massive boulder.""",
            routes=[
                Route(1, "stream", "Cross back to the north bank", danger_level=0),
                Route(2, "animal_den", "Follow the animal trail south", danger_level=2),
                Route(3, "stream_bend", "Follow the stream east around the boulder", danger_level=1),
            ],
            items=[ItemFactory.create_item("silver ore"), ItemFactory.create_item("stone")],
            features=["rocky outcroppings", "fast water", "muddy banks", "animal tracks"],
            ambient_sounds=["rushing water", "animal calls"]
        )
        
        locations["stream_bend"] = Location(
            location_id="stream_bend",
            name="Stream Bend",
            description="The stream curves sharply here around a massive boulder.",
            long_description="""A huge boulder, probably deposited here in some ancient flood, forces 
the stream to curve sharply. The water has carved a deep pool here over 
countless years. You can see the dark shapes of larger fish in the depths.

The most interesting feature is what appears to be a small opening behind 
the cascade of water flowing over the boulder - a hidden cave entrance.""",
            routes=[
                Route(1, "stream_south", "Go back west along the stream", danger_level=0),
                Route(2, "stream_falls", "Continue south where the stream drops down", danger_level=2),
                Route(3, "hidden_cave", "Slip behind the waterfall into the hidden cave", danger_level=1),
            ],
            features=["deep pool", "massive boulder", "small waterfall", "hidden entrance"],
            ambient_sounds=["waterfall splashing", "echoing water sounds"],
            water=True
        )
        
        locations["hidden_cave"] = Location(
            location_id="hidden_cave",
            name="Hidden Cave",
            description="A small cave hidden behind the waterfall.",
            long_description="""Water drips constantly from the cave ceiling, and the roar of the 
waterfall is muffled but ever-present. The cave is small but dry once 
you get past the entrance spray.

In a corner, you spot what looks like an old chest, covered in moss and 
rust. The walls are covered with strange markings - they look ancient, 
possibly older than human civilization. A dark passage leads deeper 
into the earth.""",
            routes=[
                Route(1, "stream_bend", "Exit back through the waterfall", danger_level=0),
                Route(2, "underground_passage", "Explore the dark passage deeper into the cave", 
                      danger_level=3, requires_item="torch"),
                Route(3, "chest_area", "Examine the old chest", danger_level=0),
            ],
            items=[ItemFactory.create_item("lantern")],
            features=["old chest", "strange markings", "dripping water", "dark passage"],
            dark=True,
            ambient_sounds=["dripping water", "distant rumbling", "waterfall echo"]
        )
        
        locations["chest_area"] = Location(
            location_id="chest_area",
            name="The Old Chest",
            description="Standing before the moss-covered chest.",
            long_description="""The chest is old - very old. The metal fittings have rusted almost 
completely away, but the wood remains intact, possibly preserved by 
some enchantment.

A simple lock secures the lid, green with verdigris. The strange markings 
on the walls seem to point toward this chest, as if it were the center 
of some ancient ritual.""",
            routes=[
                Route(1, "hidden_cave", "Step back from the chest", danger_level=0),
            ],
            items=[ItemFactory.create_item("old journal"), ItemFactory.create_item("ancient amulet"),
                   ItemFactory.create_item("gold coins")],
            features=["ancient chest", "ritual markings", "magical aura"],
            special_actions=["open chest", "pick lock"],
            dark=True
        )
        
        # ===================================================================
        # UNDERGROUND AREAS
        # ===================================================================
        locations["underground_passage"] = Location(
            location_id="underground_passage",
            name="Underground Passage",
            description="A dark tunnel leading deeper underground.",
            long_description="""The passage is narrow and twisting, carved by water over countless millennia. 
The air is damp and cold, carrying a musty smell of earth and stone. 
You must proceed carefully to avoid slipping on the wet stone.

Your light creates dancing shadows on the walls. You can hear water 
dripping somewhere ahead, and occasionally the distant sound of 
something moving in the darkness.

The passage branches - one way seems to lead up toward fresh air, 
while the other descends further into the earth.""",
            routes=[
                Route(1, "hidden_cave", "Return to the hidden cave", danger_level=0),
                Route(2, "cave_exit", "Take the passage leading up", danger_level=1),
                Route(3, "underground_lake", "Descend deeper into the darkness", danger_level=4),
                Route(4, "crystal_cavern", "Squeeze through a narrow side passage", 
                      danger_level=2, requires_skill=(SkillType.CLIMBING, 3)),
            ],
            creatures=[CreatureFactory.create_creature("giant spider")],
            features=["narrow passage", "wet stone", "mineral deposits", "branching tunnels"],
            dark=True,
            dangerous=True,
            danger_level=3,
            ambient_sounds=["echoing drips", "distant water", "your own footsteps", "skittering sounds"]
        )
        
        locations["crystal_cavern"] = Location(
            location_id="crystal_cavern",
            name="Crystal Cavern",
            description="A cavern filled with glittering crystals of all colors.",
            long_description="""You emerge into a breathtaking sight - a cavern filled with crystals 
of every imaginable color. They grow from the walls, ceiling, and floor, 
some as small as your finger, others as tall as a person.

The crystals catch and multiply any light source, creating a dazzling 
display that illuminates the entire cavern. Some of the crystals emit 
a faint glow of their own, filling the space with soft, ethereal light.

In the center of the cavern, a particularly large crystal formation 
pulses with inner light.""",
            routes=[
                Route(1, "underground_passage", "Squeeze back through the narrow passage", danger_level=1),
                Route(2, "crystal_throne", "Approach the large central crystal", danger_level=0),
            ],
            items=[ItemFactory.create_item("glowing crystal"), ItemFactory.create_item("gemstone"),
                   ItemFactory.create_item("ember crystal"), ItemFactory.create_item("frost shard")],
            features=["colorful crystals", "natural light", "central formation", "crystal throne"],
            ambient_sounds=["crystal humming", "magical resonance"]
        )
        
        locations["crystal_throne"] = Location(
            location_id="crystal_throne",
            name="Crystal Throne",
            description="A throne made entirely of fused crystals.",
            long_description="""The central formation is actually a throne, carved or grown from 
a massive crystal cluster. It pulses with magical energy that you 
can feel tingling on your skin.

Something rests on the seat of the throne - an object that radiates 
power. The crystals around it seem to grow toward it, as if drawn 
by its presence.""",
            routes=[
                Route(1, "crystal_cavern", "Step back from the throne", danger_level=0),
            ],
            items=[ItemFactory.create_item("enchanted staff")],
            features=["crystal throne", "magical aura", "artifact"],
            ambient_sounds=["powerful humming", "energy crackling"]
        )
        
        locations["underground_lake"] = Location(
            location_id="underground_lake",
            name="Underground Lake",
            description="A vast underground cavern containing a dark, still lake.",
            long_description="""The passage opens into an enormous cavern that takes your breath away. 
Before you stretches a dark, perfectly still lake that reflects your 
light like a black mirror. Stalactites hang from the ceiling like 
stone fangs, and bioluminescent mushrooms provide an eerie blue-green 
glow along the shores.

The silence here is absolute, broken only by the occasional drip of 
water echoing across the cavern. On a small island in the center of 
the lake, you can see something glinting.

A narrow ledge circles the lake along the cavern wall, and an old 
wooden boat is tied to a natural stone pier.""",
            routes=[
                Route(1, "underground_passage", "Return through the passage", danger_level=2),
                Route(2, "lake_ledge", "Carefully traverse the narrow ledge", 
                      danger_level=3, requires_skill=(SkillType.CLIMBING, 2)),
                Route(3, "lake_boat", "Take the boat across the lake", danger_level=2),
                Route(4, "lake_dive", "Dive into the dark water", 
                      danger_level=4, requires_skill=(SkillType.SWIMMING, 4)),
            ],
            creatures=[CreatureFactory.create_creature("ghost")],
            features=["dark lake", "stalactites", "glowing mushrooms", "island", "old boat"],
            dark=True,
            dangerous=True,
            danger_level=4,
            water=True,
            swimmable=True,
            ambient_sounds=["dripping water", "distant echoes", "unearthly whispers"]
        )
        
        locations["lake_ledge"] = Location(
            location_id="lake_ledge",
            name="Lake Ledge",
            description="A narrow ledge circling the underground lake.",
            long_description="""The ledge is barely wide enough to walk on - one wrong step and 
you'll plunge into the dark water below. You press yourself against 
the cold stone wall and inch forward carefully.

Halfway around, you spot a skeleton slumped against the wall, still 
clutching something in its bony hand. The ledge continues toward a 
natural stone bridge that extends toward the island.""",
            routes=[
                Route(1, "underground_lake", "Carefully return to the shore", danger_level=2),
                Route(2, "lake_island", "Cross the natural bridge to the island", danger_level=2),
                Route(3, "skeleton_remains", "Examine the skeleton", danger_level=0),
            ],
            items=[ItemFactory.create_item("silver dagger")],
            features=["narrow ledge", "skeleton", "natural bridge"],
            dark=True,
            dangerous=True,
            danger_level=3,
            ambient_sounds=["water lapping", "stone crumbling"]
        )
        
        locations["skeleton_remains"] = Location(
            location_id="skeleton_remains",
            name="Skeleton Remains",
            description="The remains of an unfortunate adventurer.",
            long_description="""The skeleton has been here for a very long time - years, maybe decades. 
The clothing has rotted away, but some equipment remains.

In one bony hand, the skeleton clutches a silver dagger with strange 
engravings. Around its neck hangs a tarnished medallion. A rotted 
leather pouch at its belt still contains a few items.

A journal lies nearby, its pages water-damaged but partially readable.""",
            routes=[
                Route(1, "lake_ledge", "Return to the ledge", danger_level=0),
            ],
            items=[ItemFactory.create_item("map fragment"), ItemFactory.create_item("gold coins"),
                   ItemFactory.create_item("ancient amulet")],
            features=["skeleton", "old equipment", "water-damaged journal"],
            dark=True
        )
        
        locations["lake_boat"] = Location(
            location_id="lake_boat",
            name="On the Lake",
            description="Rowing across the dark underground lake.",
            long_description="""The old boat creaks alarmingly but holds together as you push off 
from the shore. The oars dip into water so still and dark it might 
as well be ink.

The silence is oppressive. Occasionally, you see something move in 
the depths - a pale flash of something large circling below the boat.

The island grows closer, and you can now see that the glinting light 
comes from an altar of some kind.""",
            routes=[
                Route(1, "underground_lake", "Row back to the shore", danger_level=1),
                Route(2, "lake_island", "Continue to the island", danger_level=1),
            ],
            features=["old boat", "dark water", "something in the depths"],
            dark=True,
            water=True,
            dangerous=True,
            ambient_sounds=["oars splashing", "creaking wood", "something moving below"]
        )
        
        locations["lake_dive"] = Location(
            location_id="lake_dive",
            name="Lake Depths",
            description="Swimming through the cold, dark water.",
            long_description="""The water is shockingly cold, and utterly dark once you dive below 
the surface. You can feel the pressure increasing as you descend.

Your hands touch something on the lake bottom - it feels like stone 
ruins, ancient structures that predate the cavern itself. Among the 
stones, your fingers close around something metallic.""",
            routes=[
                Route(1, "underground_lake", "Surface and return to shore", danger_level=2),
            ],
            items=[ItemFactory.create_item("golden key"), ItemFactory.create_item("ancient artifact")],
            features=["underwater ruins", "cold darkness", "sunken treasure"],
            dark=True,
            water=True,
            dangerous=True,
            danger_level=5
        )
        
        locations["lake_island"] = Location(
            location_id="lake_island",
            name="Lake Island",
            description="A small island in the center of the underground lake.",
            long_description="""The island is just a mound of rock rising from the dark water, 
barely twenty feet across. In its center stands an ancient altar 
carved from a single block of black stone, covered in runes that 
seem to writhe in your peripheral vision.

On the altar rests a glowing crystal that pulses with inner light, 
and beside it, a tome bound in what looks disturbingly like skin. 
The air here feels charged with ancient power.""",
            routes=[
                Route(1, "lake_ledge", "Return via the stone bridge", danger_level=2),
                Route(2, "lake_boat", "Return to the boat", danger_level=1),
            ],
            items=[ItemFactory.create_item("glowing crystal"), ItemFactory.create_item("spirit essence")],
            features=["ancient altar", "strange runes", "glowing crystal", "skin-bound tome"],
            dark=True,
            ambient_sounds=["magical humming", "whispered words"]
        )
        
        locations["cave_exit"] = Location(
            location_id="cave_exit",
            name="Cave Exit",
            description="A narrow opening leading out of the cave.",
            long_description="""Daylight streams in through a narrow crack in the rock, almost 
blinding after the darkness of the underground. Fresh air fills 
your lungs - air that smells of flowers and growing things.

You'll have to squeeze through, but you can definitely fit. Beyond, 
you can see green foliage bathed in sunlight - somewhere very 
different from where you started.""",
            routes=[
                Route(1, "underground_passage", "Return to the underground passage", danger_level=1),
                Route(2, "sacred_grove", "Squeeze through to the outside", danger_level=0),
            ],
            features=["narrow crack", "daylight", "roots hanging", "fresh air"],
            climbable=True,
            ambient_sounds=["wind whistling", "birds outside"]
        )
        
        # ===================================================================
        # WATERFALL AREA
        # ===================================================================
        locations["waterfall"] = Location(
            location_id="waterfall",
            name="Cascading Waterfall",
            description="A beautiful waterfall cascades down from rocky cliffs above.",
            long_description="""A magnificent waterfall plunges down from the cliffs in a thunder 
of white water, creating a perpetual mist that catches the light in 
rainbow arcs. The roar of the falling water is almost deafening, 
filling the air with a constant, powerful sound.

The pool at the base of the waterfall is deep and clear, fed by the 
endless cascade. A narrow, treacherous path climbs up alongside the 
falls, slick with spray. Behind the curtain of water, you notice 
what might be a dark opening - another cave.""",
            routes=[
                Route(1, "stream", "Follow the stream back south", danger_level=0),
                Route(2, "cliff_top", "Climb the dangerous path to the cliff top", 
                      danger_level=3, requires_skill=(SkillType.CLIMBING, 3)),
                Route(3, "waterfall_cave", "Go behind the waterfall into the cave", danger_level=1),
                Route(4, "waterfall_pool", "Swim in the pool beneath the falls", 
                      danger_level=1, requires_skill=(SkillType.SWIMMING, 2)),
            ],
            items=[ItemFactory.create_item("healing herb"), ItemFactory.create_item("healing herb")],
            features=["waterfall", "rainbow mist", "deep pool", "hidden cave entrance", "climbing path"],
            water=True,
            climbable=True,
            ambient_sounds=["roaring water", "splashing", "wind from falls"]
        )
        
        locations["waterfall_pool"] = Location(
            location_id="waterfall_pool",
            name="Waterfall Pool",
            description="Swimming in the pool beneath the thundering waterfall.",
            long_description="""The water is cold but refreshing. You can feel the power of the 
waterfall churning the pool, creating strong currents that pull at 
you. The mist rising from the impact zone creates a constant spray.

Something glitters at the bottom of the pool - it looks like someone 
lost something valuable here long ago.""",
            routes=[
                Route(1, "waterfall", "Swim back to shore", danger_level=0),
            ],
            items=[ItemFactory.create_item("gemstone"), ItemFactory.create_item("gold coins")],
            features=["churning water", "underwater glinting", "strong currents"],
            water=True,
            swimmable=True,
            ambient_sounds=["underwater rumbling", "muffled waterfall"]
        )
        
        locations["waterfall_cave"] = Location(
            location_id="waterfall_cave",
            name="Cave Behind the Waterfall",
            description="A damp cave hidden behind the thundering waterfall.",
            long_description="""The cave is perpetually damp from the spray of the waterfall. The 
thundering sound is muffled here but still omnipresent, a constant 
vibration you feel in your bones.

Old, rotted wooden crates lie scattered about - someone used this 
place as a hiding spot long ago, perhaps smugglers or bandits. Among 
the debris, you notice some supplies that are still intact.

Strange symbols are painted on the back wall in what looks like dried 
blood, forming patterns that hurt to look at directly.""",
            routes=[
                Route(1, "waterfall", "Exit back through the waterfall", danger_level=0),
                Route(2, "smuggler_cache", "Search the old crates thoroughly", danger_level=0),
            ],
            items=[ItemFactory.create_item("rope"), ItemFactory.create_item("dried meat"),
                   ItemFactory.create_item("torch"), ItemFactory.create_item("gold coins")],
            features=["rotted crates", "old supplies", "blood symbols", "damp walls"],
            dark=True,
            ambient_sounds=["muffled waterfall", "dripping water"]
        )
        
        locations["smuggler_cache"] = Location(
            location_id="smuggler_cache",
            name="Smuggler's Hidden Cache",
            description="A hidden compartment behind the rotted crates.",
            long_description="""Behind the old crates, hidden by a loose stone, you find a small 
chamber carved into the rock. This was clearly the smugglers' real 
treasure hiding spot.

Inside, you find several valuable items that have been preserved 
from the damp by oiled leather wrappings. There's also a journal 
written in a shaky hand - the last words of someone who never 
escaped these woods.""",
            routes=[
                Route(1, "waterfall_cave", "Return to the main cave", danger_level=0),
            ],
            items=[ItemFactory.create_item("chainmail"), ItemFactory.create_item("gold coins"),
                   ItemFactory.create_item("healing potion"), ItemFactory.create_item("thieves tools")],
            features=["hidden compartment", "oiled leather wrappings", "smuggler's journal"],
            dark=True
        )
        
        locations["cliff_top"] = Location(
            location_id="cliff_top",
            name="Cliff Top",
            description="The top of the cliff overlooking the waterfall and forest below.",
            long_description="""You stand at the top of the cliff, spray from the waterfall 
dampening your clothes. From this height, you can see for miles 
in every direction. The forest stretches like a green ocean, 
broken only by a few landmarks.

To the north, a stone tower rises above the trees, ancient and 
imposing. To the east, the forest gives way to dead, blackened 
trees - a place of decay. To the west, mountains rise in the 
distance, their peaks lost in clouds.

A rope bridge spans a deep gorge to the north, swaying in the wind.""",
            routes=[
                Route(1, "waterfall", "Climb back down to the waterfall", danger_level=2),
                Route(2, "rope_bridge", "Cross the rope bridge north", danger_level=2),
                Route(3, "dead_forest_edge", "Head east toward the dead forest", danger_level=3),
                Route(4, "mountain_path", "Take the path toward the mountains", danger_level=2),
            ],
            items=[ItemFactory.create_item("feather"), ItemFactory.create_item("feather"),
                   ItemFactory.create_item("compass")],
            features=["panoramic view", "rope bridge", "stone tower in distance", "gorge"],
            ambient_sounds=["wind whistling", "distant eagles", "creaking rope bridge"]
        )
        
        # ===================================================================
        # DARK WOODS AREA
        # ===================================================================
        locations["dark_woods"] = Location(
            location_id="dark_woods",
            name="Dark Woods",
            description="The forest grows darker here. Ancient trees block out most of the light.",
            long_description="""Massive, ancient trees tower overhead, their branches intertwining 
to form a nearly solid canopy. Very little light penetrates to the 
forest floor, creating an atmosphere of perpetual twilight. The air 
is still and heavy, and an oppressive silence hangs over everything.

Strange mushrooms grow in clusters along the roots of the trees, some 
faintly glowing with an otherworldly phosphorescence. Spider webs 
glisten between the branches, some large enough to trap a person.

Multiple paths lead away through the shadows, each seeming as 
treacherous as the last.""",
            routes=[
                Route(1, "clearing", "Return south to the clearing", danger_level=0),
                Route(2, "hermit_hut", "Follow the faint light northeast", danger_level=1),
                Route(3, "deep_woods", "Continue northwest into the deeper darkness", danger_level=4),
                Route(4, "mushroom_circle", "Investigate the glowing mushrooms to the east", danger_level=2),
                Route(5, "spider_nest", "Enter the area thick with webs", danger_level=4),
                Route(6, "wolf_den", "Follow the animal tracks west", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("wolf"), CreatureFactory.create_creature("giant spider")],
            items=[ItemFactory.create_item("mushroom"), ItemFactory.create_item("wood")],
            features=["massive trees", "glowing mushrooms", "spider webs", "oppressive silence"],
            dark=True,
            dangerous=True,
            danger_level=2,
            ambient_sounds=["distant howling", "creaking branches", "unnatural silence"]
        )
        
        locations["wolf_den"] = Location(
            location_id="wolf_den",
            name="Wolf Den",
            description="A hollow beneath massive tree roots serves as a wolf den.",
            long_description="""The forest opens into a small depression where the roots of several 
ancient trees have created natural caves and shelters. This is clearly 
a wolf den - you can see gnawed bones scattered about, and the strong 
smell of animals fills the air.

Several wolves eye you warily, some growling low in their throats. 
The alpha, a massive grey wolf with scarred flanks, watches you with 
intelligent, calculating eyes.""",
            routes=[
                Route(1, "dark_woods", "Back away slowly toward the dark woods", danger_level=2),
                Route(2, "wolf_alpha", "Approach the alpha wolf", danger_level=4),
            ],
            creatures=[CreatureFactory.create_creature("wolf"), CreatureFactory.create_creature("wolf"),
                      CreatureFactory.create_creature("dire wolf")],
            items=[ItemFactory.create_item("wolf pelt")],
            features=["root caves", "gnawed bones", "wolf pack", "alpha wolf"],
            dangerous=True,
            danger_level=4,
            ambient_sounds=["growling", "panting", "bones crunching"]
        )
        
        locations["wolf_alpha"] = Location(
            location_id="wolf_alpha",
            name="Before the Alpha",
            description="Standing before the massive alpha wolf.",
            long_description="""The alpha wolf is huge - larger than any wolf you've ever seen or 
heard of. Its grey fur is marked with countless battle scars, and 
its yellow eyes seem to hold an almost human intelligence.

It doesn't attack immediately. Instead, it seems to be... waiting. 
Testing you. Perhaps there is a way to earn its respect rather 
than fight it.""",
            routes=[
                Route(1, "wolf_den", "Back away from the alpha", danger_level=1),
            ],
            creatures=[CreatureFactory.create_creature("dire wolf")],
            items=[ItemFactory.create_item("lucky charm")],
            features=["alpha wolf", "intelligent eyes", "test of will"],
            dangerous=True,
            danger_level=5,
            special_actions=["submit", "challenge", "offer food"]
        )
        
        locations["spider_nest"] = Location(
            location_id="spider_nest",
            name="Spider Nest",
            description="The trees here are completely wrapped in thick spider webs.",
            long_description="""Every surface is covered in sticky, rope-thick webbing. The trees 
themselves are barely visible beneath layers of silk. Desiccated 
husks of animals - and what might be people - hang wrapped in 
cocoons from the branches.

You can feel vibrations in the web as you move, and you know something 
is aware of your presence. Multiple pairs of eyes glint in the darkness.

At the center of the web, a massive shape waits...""",
            routes=[
                Route(1, "dark_woods", "Carefully retreat from the webs", danger_level=2),
                Route(2, "spider_queen_lair", "Push deeper toward the center", danger_level=5),
            ],
            creatures=[CreatureFactory.create_creature("giant spider"), CreatureFactory.create_creature("giant spider")],
            items=[ItemFactory.create_item("spider silk"), ItemFactory.create_item("spider silk")],
            features=["thick webs", "wrapped victims", "watching eyes", "massive shape"],
            dark=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["skittering", "web vibrating", "chittering"]
        )
        
        locations["spider_queen_lair"] = Location(
            location_id="spider_queen_lair",
            name="Spider Queen's Lair",
            description="The heart of the spider nest, where the Queen dwells.",
            long_description="""The Spider Queen is a nightmare made flesh - a spider the size of 
a horse, her bloated abdomen pulsing with eggs. Eight eyes the size 
of plates fix upon you with alien hunger.

Around her, dozens of smaller spiders wait for her command. The web 
here is so thick it forms platforms and tunnels, a city of silk 
devoted to this monstrous creature.

Beneath her, you can see the remains of her victims... and among 
them, something that gleams with magical light.""",
            routes=[
                Route(1, "spider_nest", "Try to escape back through the webs", danger_level=4),
            ],
            creatures=[CreatureFactory.create_creature("spider queen")],
            items=[ItemFactory.create_item("ring of regeneration"), ItemFactory.create_item("spider silk"),
                   ItemFactory.create_item("spider silk"), ItemFactory.create_item("spider silk")],
            features=["spider queen", "egg sacs", "web city", "magical gleam"],
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["chittering horde", "egg sacs pulsing", "queen's hiss"]
        )
        
        locations["mushroom_circle"] = Location(
            location_id="mushroom_circle",
            name="Mushroom Circle",
            description="A perfect circle of giant mushrooms in a small clearing.",
            long_description="""In this small clearing, giant mushrooms form a perfect circle - 
too perfect to be natural. The largest stand taller than you, their 
caps wide enough to shelter beneath. A strange mist hovers just 
above the ground, swirling in patterns that seem almost deliberate.

The air feels different here - charged with something ancient and 
otherworldly. The hair on your arms stands on end, and you have 
the unmistakable feeling of being watched, though you see no one.

Faint music seems to come from nowhere and everywhere at once.""",
            routes=[
                Route(1, "dark_woods", "Leave the circle to the west", danger_level=0),
                Route(2, "fairy_grove", "Follow the faint path east toward the music", danger_level=1),
                Route(3, "mushroom_center", "Step into the center of the circle", danger_level=2),
            ],
            features=["giant mushrooms", "strange mist", "magical aura", "faint music"],
            ambient_sounds=["ethereal music", "whispers in unknown language", "wind chimes"]
        )
        
        locations["mushroom_center"] = Location(
            location_id="mushroom_center",
            name="Center of the Circle",
            description="Standing in the exact center of the mushroom ring.",
            long_description="""The moment you step into the center of the circle, the world seems 
to shift. The colors become more vivid, the sounds more clear. The 
mushrooms seem to lean toward you, and the mist swirls faster.

You feel a presence - something ancient and powerful considering you.

Words form in your mind, not heard but understood: "Why have you 
come to our circle, mortal? What do you seek?"

You sense this could be very dangerous... or very rewarding.""",
            routes=[
                Route(1, "mushroom_circle", "Step out of the circle", danger_level=0),
            ],
            features=["magical focus", "presence", "vivid colors", "swirling mist"],
            special_actions=["answer truthfully", "lie", "offer gift", "demand power"],
            ambient_sounds=["otherworldly humming", "whispered words"]
        )
        
        locations["fairy_grove"] = Location(
            location_id="fairy_grove",
            name="Fairy Grove",
            description="A magical grove filled with dancing lights.",
            long_description="""Tiny lights dance through the air like living stars, leaving 
trails of sparkles in their wake. The plants here seem more 
vibrant, more alive than anywhere else in the forest. Flowers 
bloom in impossible colors - blues that sing and purples that 
whisper.

A delicate throne made of twisted living branches sits in the 
center of the grove, and upon it sits a being of otherworldly 
beauty - humanoid but not human, with skin that shimmers like 
moonlight on water and eyes like pools of starlight.

This is the court of the Fairy Queen.""",
            routes=[
                Route(1, "mushroom_circle", "Return to the mushroom circle", danger_level=0),
                Route(2, "fairy_throne", "Approach the Fairy Queen's throne", danger_level=1),
                Route(3, "fairy_market", "Visit the fairy market", danger_level=0),
            ],
            creatures=[CreatureFactory.create_creature("tree spirit")],
            items=[ItemFactory.create_item("lucky charm"), ItemFactory.create_item("healing potion")],
            features=["dancing lights", "vibrant plants", "branch throne", "impossible flowers", "fairy queen"],
            ambient_sounds=["tinkling bells", "melodic humming", "gentle laughter"]
        )
        
        locations["fairy_throne"] = Location(
            location_id="fairy_throne",
            name="Before the Fairy Queen",
            description="Standing before the throne of the Fairy Queen.",
            long_description="""The Fairy Queen regards you with ancient, amused eyes. Though she 
appears young and beautiful, you sense she has lived for thousands 
of years. Her voice, when she speaks, sounds like wind through 
crystal chimes.

"A mortal in my grove. How... quaint. Tell me, little one, what 
brings you to our realm? Speak truly, for lies have no power here."

Around her, the tiny lights cluster and watch, and you sense any 
wrong move could be your last.""",
            routes=[
                Route(1, "fairy_grove", "Step back from the throne", danger_level=0),
            ],
            features=["fairy queen", "watching lights", "ancient power"],
            special_actions=["request help", "offer service", "ask about forest"],
            ambient_sounds=["crystal chimes", "whispered judgment"]
        )
        
        locations["fairy_market"] = Location(
            location_id="fairy_market",
            name="Fairy Market",
            description="A magical marketplace where fairies trade in strange goods.",
            long_description="""The market is a chaotic swirl of lights, sounds, and impossible 
objects. Fairies of all shapes and sizes hawk their wares from 
stalls made of mushroom caps and flower petals.

They trade in things mortals rarely deal with: bottled moonlight, 
jars of forgotten dreams, scales from fish that never existed. 
But they also have more practical goods - potions, weapons, and 
strange artifacts.

Be warned: fairy deals always have a catch.""",
            routes=[
                Route(1, "fairy_grove", "Return to the main grove", danger_level=0),
            ],
            items=[ItemFactory.create_item("invisibility potion"), ItemFactory.create_item("boots of speed")],
            features=["fairy stalls", "strange goods", "chaotic atmosphere", "trading fairies"],
            shop_available=True,
            ambient_sounds=["haggling", "tinkling", "magical chimes"]
        )
        
        # ===================================================================
        # HERMIT'S AREA
        # ===================================================================
        locations["hermit_hut"] = Location(
            location_id="hermit_hut",
            name="Hermit's Hut",
            description="A small, ramshackle hut built against a massive tree.",
            long_description="""A crude hut made of branches, leaves, and salvaged wood leans 
against an enormous oak tree. Smoke rises from a crooked chimney, 
and strange herbs hang drying from the eaves. The smell of wood 
smoke and cooking food drifts through the air.

A garden of medicinal plants grows in carefully tended beds around 
the hut. Whoever lives here must know the forest well - and how 
to survive in it.

The door stands slightly ajar, and you can hear someone humming 
inside.""",
            routes=[
                Route(1, "dark_woods", "Return to the dark woods", danger_level=0),
                Route(2, "hermit_interior", "Enter the hut", danger_level=0),
                Route(3, "hermit_garden", "Examine the herb garden", danger_level=0),
            ],
            creatures=[CreatureFactory.create_creature("hermit")],
            features=["crude hut", "herb garden", "massive oak", "smoking chimney"],
            ambient_sounds=["crackling fire", "humming", "wind chimes"],
            rest_allowed=True,
            save_point=True
        )
        
        locations["hermit_interior"] = Location(
            location_id="hermit_interior",
            name="Inside the Hermit's Hut",
            description="The cluttered interior of the hermit's home.",
            long_description="""The inside of the hut is a organized chaos of herbs, books, and 
strange artifacts. Bundles of dried plants hang from every beam, 
and shelves overflow with jars containing things you'd rather not 
examine too closely.

An old man sits by the fire, stirring a pot of something that 
smells surprisingly delicious. His eyes, bright and sharp despite 
his weathered face, regard you with curiosity rather than fear.

"Sit, sit," he says. "You look like you could use a warm meal 
and some answers. I have both."
            """,
            routes=[
                Route(1, "hermit_hut", "Exit the hut", danger_level=0),
            ],
            creatures=[CreatureFactory.create_creature("hermit")],
            items=[ItemFactory.create_item("healing herb"), ItemFactory.create_item("map fragment"),
                   ItemFactory.create_item("dried meat")],
            features=["dried herbs", "mysterious jars", "old books", "warm fire", "cooking pot"],
            ambient_sounds=["fire crackling", "pot bubbling", "hermit humming"]
        )
        
        locations["hermit_garden"] = Location(
            location_id="hermit_garden",
            name="Hermit's Garden",
            description="A well-tended garden of medicinal plants.",
            long_description="""The garden is a treasure trove of useful plants - herbs for healing, 
roots for poisons (and their antidotes), flowers that can ease pain 
or bring vivid dreams.

Everything is carefully labeled in a cramped but readable hand. 
You could gather some supplies here, but taking too much would be 
stealing from the hermit who tends them.""",
            routes=[
                Route(1, "hermit_hut", "Return to the front of the hut", danger_level=0),
            ],
            items=[ItemFactory.create_item("healing herb"), ItemFactory.create_item("healing herb"),
                   ItemFactory.create_item("antidote")],
            features=["medicinal plants", "labeled sections", "careful cultivation"],
            ambient_sounds=["bees buzzing", "wind in leaves"]
        )
        
        # ===================================================================
        # DEEP WOODS AREA
        # ===================================================================
        locations["deep_woods"] = Location(
            location_id="deep_woods",
            name="Deep Woods",
            description="The darkest part of the forest, where ancient things dwell.",
            long_description="""This is the heart of the forest, where light never reaches and 
ancient things dwell in eternal shadow. The trees here are twisted 
and gnarled, their bark black as coal, their branches reaching 
like grasping claws.

The air is thick with the smell of rot and old magic. You can feel 
eyes watching you from the darkness - many eyes, hungry eyes. This 
is not a place for mortals.

Strange sounds echo through the darkness - whispers, growls, and 
something that might be laughter.""",
            routes=[
                Route(1, "dark_woods", "Retreat to the lighter woods", danger_level=2),
                Route(2, "ancient_ruins", "Follow the stone path to ancient ruins", danger_level=4),
                Route(3, "corrupted_grove", "Enter the place where the trees are dying", danger_level=5),
                Route(4, "shadow_pool", "Investigate the pool of darkness", danger_level=5),
            ],
            creatures=[CreatureFactory.create_creature("wraith"), CreatureFactory.create_creature("skeleton")],
            features=["twisted trees", "eternal shadow", "watching eyes", "ancient presence"],
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["whispers", "growling", "unnatural laughter", "branches scraping"]
        )
        
        locations["ancient_ruins"] = Location(
            location_id="ancient_ruins",
            name="Ancient Ruins",
            description="Crumbling ruins of a civilization long forgotten.",
            long_description="""Stone walls rise from the forest floor, covered in moss and vines 
but unmistakably the work of intelligent hands. This was once a 
great building - a temple, perhaps, or a palace.

The architecture is strange, the proportions somehow wrong for human 
builders. Carvings on the remaining walls show beings that might be 
gods or might be demons, engaged in acts of creation and destruction.

At the center of the ruins, stairs lead down into darkness.""",
            routes=[
                Route(1, "deep_woods", "Return to the deep woods", danger_level=3),
                Route(2, "ruined_temple", "Descend the stairs into darkness", 
                      danger_level=5, requires_item="torch"),
                Route(3, "ruin_library", "Explore the collapsed eastern wing", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("skeleton"), CreatureFactory.create_creature("ghost")],
            items=[ItemFactory.create_item("ancient amulet"), ItemFactory.create_item("stone")],
            features=["crumbling walls", "strange carvings", "descending stairs", "ancient architecture"],
            dark=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["stone crumbling", "wind through gaps", "distant chanting"]
        )
        
        locations["ruin_library"] = Location(
            location_id="ruin_library",
            name="Ruined Library",
            description="The remains of an ancient library, books turned to dust.",
            long_description="""This was once a great library, but time has destroyed almost 
everything. Shelves have collapsed, and most books have rotted 
to nothing. The smell of ancient paper and decay fills the air.

But not everything is lost. Some books were stored in sealed 
cases, protected from the elements. And one section of wall 
is covered in carved text that remains perfectly legible - a 
spell or perhaps a warning.""",
            routes=[
                Route(1, "ancient_ruins", "Return to the main ruins", danger_level=2),
            ],
            items=[ItemFactory.create_item("old journal"), ItemFactory.create_item("mana potion")],
            features=["collapsed shelves", "sealed cases", "carved text", "preserved books"],
            dark=True,
            ambient_sounds=["pages rustling", "settling stone"]
        )
        
        locations["ruined_temple"] = Location(
            location_id="ruined_temple",
            name="Ruined Temple",
            description="The underground remains of an ancient temple.",
            long_description="""The stairs lead down into a vast underground chamber - a temple 
to gods no longer worshipped. Massive pillars support a ceiling 
lost in shadow, and at the far end, an altar still stands before 
a statue of something you cannot quite comprehend.

The statue seems to shift when you're not looking directly at it. 
Its many arms hold symbols of power, and its face... its face is 
wrong in ways that hurt to contemplate.

Bones litter the floor - offerings, or sacrifices?""",
            routes=[
                Route(1, "ancient_ruins", "Climb back up the stairs", danger_level=2),
                Route(2, "temple_altar", "Approach the altar", danger_level=5),
                Route(3, "temple_catacombs", "Enter the catacombs behind the altar", danger_level=5),
            ],
            creatures=[CreatureFactory.create_creature("skeleton"), CreatureFactory.create_creature("skeleton"),
                      CreatureFactory.create_creature("ghost")],
            items=[ItemFactory.create_item("gold coins"), ItemFactory.create_item("spirit essence")],
            features=["massive pillars", "impossible statue", "bone-covered floor", "ancient altar"],
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["whispered prayers", "bone rattling", "something breathing"]
        )
        
        locations["temple_altar"] = Location(
            location_id="temple_altar",
            name="Before the Altar",
            description="Standing before the altar of a forgotten god.",
            long_description="""The altar is stained with ancient blood, layer upon layer of 
sacrifices offered to the thing represented by the statue. Power 
radiates from this place - dark, hungry power that calls to 
something deep within you.

On the altar rest several objects: a chalice filled with liquid 
darkness, a knife made of obsidian, and a book bound in something 
that might be human skin.

You feel the presence of the god, dead or sleeping, but not gone. 
It waits for a worthy servant... or a worthy sacrifice.""",
            routes=[
                Route(1, "ruined_temple", "Step back from the altar", danger_level=1),
            ],
            items=[ItemFactory.create_item("shadow dagger"), ItemFactory.create_item("shadow essence")],
            features=["blood-stained altar", "dark chalice", "skin-bound book", "divine presence"],
            dark=True,
            dangerous=True,
            danger_level=5,
            special_actions=["make offering", "drink from chalice", "read book", "reject power"],
            ambient_sounds=["divine whispers", "heartbeat", "call of darkness"]
        )
        
        locations["temple_catacombs"] = Location(
            location_id="temple_catacombs",
            name="Temple Catacombs",
            description="Ancient catacombs filled with the remains of priests and sacrifices.",
            long_description="""The catacombs stretch far into the earth, tunnel after tunnel of 
niches containing bones and funerary objects. Some of the dead were 
honored priests; others were clearly sacrifices, their bones still 
bearing the marks of ritual death.

At the deepest point of the catacombs, a heavy stone door stands 
sealed with chains of black iron. Something moves behind it, 
scratching at the stone. Something that has been trapped there 
for a very, very long time.""",
            routes=[
                Route(1, "ruined_temple", "Return to the temple chamber", danger_level=2),
                Route(2, "lich_chamber", "Break the chains and open the door", 
                      danger_level=5, requires_item="crypt key"),
            ],
            creatures=[CreatureFactory.create_creature("skeleton"), CreatureFactory.create_creature("skeleton"),
                      CreatureFactory.create_creature("wraith")],
            items=[ItemFactory.create_item("gold coins"), ItemFactory.create_item("ancient artifact")],
            features=["bone niches", "sealed door", "scratching sounds", "ritual marks"],
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["scratching", "chains rattling", "distant moaning"]
        )
        
        locations["lich_chamber"] = Location(
            location_id="lich_chamber",
            name="The Lich's Chamber",
            description="The prison of an undead sorcerer, now freed.",
            long_description="""The door swings open to reveal a chamber of horrors. This was 
both prison and throne room for one of the most powerful undead 
to ever exist - a Lich, an immortal sorcerer who traded life for 
eternal power.

It rises from its throne of bones, tattered robes swirling with 
dark energy, crown of blackened bone atop a skull that grins with 
malevolent intelligence.

"At last," it rasps, "a visitor. And you have freed me from my 
chains. How... thoughtful. Now, shall we discuss your reward?"

This will be the fight of your life.""",
            routes=[
                Route(1, "temple_catacombs", "Try to flee back through the catacombs", danger_level=4),
            ],
            creatures=[CreatureFactory.create_creature("lich")],
            items=[ItemFactory.create_item("enchanted staff"), ItemFactory.create_item("royal crown"),
                   ItemFactory.create_item("master key")],
            features=["bone throne", "lich", "dark energy", "ancient power"],
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["crackling dark energy", "skeletal laughter", "whispers of doom"]
        )
        
        locations["corrupted_grove"] = Location(
            location_id="corrupted_grove",
            name="Corrupted Grove",
            description="A dying grove where nature has been twisted by dark magic.",
            long_description="""This was once a beautiful grove, but something has corrupted it. 
The trees are dead or dying, their bark blackened and oozing foul 
liquid. The grass is brown and brittle, and the flowers have 
withered into twisted mockeries of themselves.

At the center of the corruption stands a massive tree, its trunk 
split open to reveal a pulsing darkness within. This is the source 
of the corruption - a wound in the world itself.

The Forest Guardian kneels before it, vines and roots binding it 
in place, fighting against the corruption that seeks to consume it.""",
            routes=[
                Route(1, "deep_woods", "Retreat from the corruption", danger_level=3),
                Route(2, "guardian_battle", "Approach the Guardian and the corruption", danger_level=5),
            ],
            creatures=[CreatureFactory.create_creature("swamp creature")],
            features=["dying trees", "corrupted plants", "wound in reality", "bound guardian"],
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["writhing corruption", "guardian's struggle", "dying forest"]
        )
        
        locations["guardian_battle"] = Location(
            location_id="guardian_battle",
            name="Before the Forest Guardian",
            description="Face to face with the Guardian - and the corruption controlling it.",
            long_description="""The Forest Guardian turns its ancient eyes upon you. In them, you 
see a desperate plea - it is being corrupted, forced to serve the 
darkness, but some part of it still fights.

"Help... me..." it groans, even as corruption vines try to force 
it to attack you. "The Heart... take the Heart... end this..."

You understand. To save the forest - and possibly find your way 
out - you must either destroy the Guardian to take its Heart, or 
find a way to cleanse the corruption.

Either way, battle is inevitable.""",
            routes=[
                Route(1, "corrupted_grove", "Retreat while you still can", danger_level=4),
            ],
            creatures=[CreatureFactory.create_creature("forest guardian")],
            items=[ItemFactory.create_item("forest heart"), ItemFactory.create_item("guardian token"),
                   ItemFactory.create_item("guardian blade")],
            features=["corrupted guardian", "pulsing darkness", "desperate plea"],
            dark=True,
            dangerous=True,
            danger_level=5,
            special_actions=["fight", "cleanse", "absorb corruption"],
            ambient_sounds=["guardian's groans", "corruption writhing", "nature crying"]
        )
        
        locations["shadow_pool"] = Location(
            location_id="shadow_pool",
            name="Shadow Pool",
            description="A pool of absolute darkness, deeper than it should be.",
            long_description="""In a hollow between the twisted trees lies a pool of perfect 
darkness. It's not water - it's something else entirely, something 
that devours light itself. Looking into it, you see no reflection, 
no bottom, only endless void.

Something moves within the darkness. Something vast and patient. 
Something that has waited a very long time for prey foolish enough 
to approach.

The Shadow Beast lurks here, and it has noticed you.""",
            routes=[
                Route(1, "deep_woods", "Back away slowly from the pool", danger_level=4),
                Route(2, "shadow_realm", "Dive into the shadow pool", 
                      danger_level=5, requires_item="spirit ward"),
            ],
            creatures=[CreatureFactory.create_creature("shadow beast")],
            items=[ItemFactory.create_item("shadow essence"), ItemFactory.create_item("shadow cloak")],
            features=["absolute darkness", "endless void", "lurking presence", "devoured light"],
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["void whispers", "light being consumed", "predatory patience"]
        )
        
        locations["shadow_realm"] = Location(
            location_id="shadow_realm",
            name="Shadow Realm",
            description="A dimension of pure shadow and nightmare.",
            long_description="""You fall through darkness - not just absence of light, but 
presence of darkness, a tangible force that presses against you 
from all sides. Then you land on something solid, though you 
cannot see it.

This is the shadow realm, a dimension that exists alongside the 
real world. Here, shadows are real, and light is the intruder.

But even here, some light exists. In the distance, you see a 
glimmer - a star fallen into shadow. And between you and it, 
shadows move with purpose and hunger.""",
            routes=[
                Route(1, "shadow_pool", "Find the way back to the pool", danger_level=4),
                Route(2, "fallen_star", "Journey toward the distant light", danger_level=5),
            ],
            creatures=[CreatureFactory.create_creature("wraith"), CreatureFactory.create_creature("ghost")],
            features=["tangible darkness", "shadow ground", "distant light", "moving shadows"],
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["shadow whispers", "reality bending", "distant screaming"]
        )
        
        locations["fallen_star"] = Location(
            location_id="fallen_star",
            name="The Fallen Star",
            description="A fragment of celestial light trapped in the shadow realm.",
            long_description="""Against all odds, you've reached it - a fragment of starlight 
somehow trapped in the shadow realm. It hovers above the ground, 
a sphere of pure white light that pushes back the darkness.

Touching it fills you with warmth and hope - feelings that 
have no place in the shadow realm. This is power incarnate, 
a weapon against the darkness itself.""",
            routes=[
                Route(1, "shadow_realm", "Return to the shadow realm", danger_level=3),
            ],
            items=[ItemFactory.create_item("sunstone")],
            features=["celestial light", "pure warmth", "hope manifest", "anti-shadow"],
            ambient_sounds=["celestial harmony", "shadows retreating", "light humming"]
        )
        
        # ===================================================================
        # MISTY GROVE AREA
        # ===================================================================
        locations["misty_grove"] = Location(
            location_id="misty_grove",
            name="Misty Grove",
            description="A grove perpetually shrouded in thick mist.",
            long_description="""Thick fog fills this area, reducing visibility to just a few feet. 
The mist seems almost alive, swirling and reaching with tendrils of 
vapor. Shapes move within it - or do they? It's impossible to tell 
what's real and what's imagination.

The air is damp and cold, and sounds are muffled and distorted by 
the fog. You could easily become lost here, wandering in circles 
until exhaustion takes you.

Somewhere in the mist, you hear voices calling - but whether they're 
friendly or hostile, you cannot tell.""",
            routes=[
                Route(1, "stream", "Follow the stream back west", danger_level=1),
                Route(2, "witch_hut", "Follow the voices deeper into the mist", danger_level=3),
                Route(3, "lost_in_mist", "Wander into the thick mist", danger_level=4),
                Route(4, "mist_clearing", "Push through to a clearing you glimpse ahead", danger_level=2),
            ],
            creatures=[CreatureFactory.create_creature("ghost")],
            features=["thick fog", "moving shapes", "distorted sounds", "swirling mist"],
            ambient_sounds=["voices in mist", "fog swirling", "distant calls", "muffled footsteps"],
            dangerous=True,
            danger_level=3
        )
        
        locations["lost_in_mist"] = Location(
            location_id="lost_in_mist",
            name="Lost in the Mist",
            description="Completely disoriented in the thick fog.",
            long_description="""You've lost all sense of direction. The mist is so thick you can 
barely see your own hands. Every direction looks the same - gray 
fog and shadowy shapes that disappear when you approach.

You hear footsteps around you, but when you turn, there's nothing 
there. Laughter echoes from all sides. You're being toyed with.

You need to find a way out before you're trapped here forever.""",
            routes=[
                Route(1, "misty_grove", "Try to retrace your steps", danger_level=3),
                Route(2, "ghost_circle", "Follow the laughter", danger_level=4),
                Route(3, "mist_clearing", "Push forward blindly", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("ghost"), CreatureFactory.create_creature("ghost")],
            features=["complete disorientation", "phantom sounds", "oppressive fog"],
            dangerous=True,
            danger_level=4,
            ambient_sounds=["phantom footsteps", "echoing laughter", "your own breathing"]
        )
        
        locations["ghost_circle"] = Location(
            location_id="ghost_circle",
            name="Circle of Ghosts",
            description="Surrounded by restless spirits.",
            long_description="""The mist parts slightly, and you find yourself in a circle of 
ghostly figures. They float just above the ground, their 
translucent forms flickering like candlelight.

Some weep, some rage, some simply stare with empty eyes. All are 
trapped here, unable to move on, reliving their final moments 
over and over.

One ghost approaches you, its face filled with desperate hope. 
Perhaps you can help them find peace... or perhaps they'll drag 
you into death with them.""",
            routes=[
                Route(1, "lost_in_mist", "Try to escape the circle", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("ghost"), CreatureFactory.create_creature("ghost"),
                      CreatureFactory.create_creature("wraith")],
            items=[ItemFactory.create_item("spirit essence"), ItemFactory.create_item("spirit essence")],
            features=["ghost circle", "restless spirits", "desperate hope", "endless torment"],
            dangerous=True,
            danger_level=4,
            special_actions=["help spirits", "flee", "fight"],
            ambient_sounds=["weeping", "rage", "whispered pleas"]
        )
        
        locations["mist_clearing"] = Location(
            location_id="mist_clearing",
            name="Clearing in the Mist",
            description="A small clearing where the mist thins slightly.",
            long_description="""The fog is less dense here, though still present. You can make out 
the shapes of trees and the ground beneath your feet more clearly.

In the center of the clearing stands an ancient stone marker, 
covered in moss and carved with directional symbols. This must be 
some kind of waystone, placed here long ago to guide travelers 
through the mist.

Following its directions might lead you to safety... or deeper 
into danger.""",
            routes=[
                Route(1, "misty_grove", "Follow the marker back to the grove entrance", danger_level=1),
                Route(2, "witch_hut", "Follow the marker toward the north", danger_level=2),
                Route(3, "swamp_edge", "Follow the marker toward the east", danger_level=3),
            ],
            items=[ItemFactory.create_item("compass")],
            features=["stone waymarker", "thinning mist", "directional symbols"],
            ambient_sounds=["clearer sounds", "wind moving fog"]
        )
        
        locations["witch_hut"] = Location(
            location_id="witch_hut",
            name="Witch's Hut",
            description="A crooked hut built on chicken legs.",
            long_description="""Through the mist, you spot something impossible - a hut standing 
on enormous chicken legs, like something from a dark fairy tale. 
Green smoke rises from its chimney, and strange lights flicker in 
the windows.

The hut seems to be alive, shifting its weight from foot to foot, 
turning slowly to keep an eye on you. The door is carved to look 
like a mouth with sharp teeth.

This is the home of the Forest Witch, and you can feel her power 
radiating from within.""",
            routes=[
                Route(1, "misty_grove", "Back away into the mist", danger_level=2),
                Route(2, "witch_interior", "Knock on the door", danger_level=0),
                Route(3, "witch_garden", "Sneak around to the back garden", danger_level=1),
            ],
            creatures=[CreatureFactory.create_creature("witch")],
            features=["chicken-leg hut", "green smoke", "living building", "tooth-door"],
            ambient_sounds=["cackling", "bubbling cauldron", "creaking wood"],
            shop_available=True
        )
        
        locations["witch_interior"] = Location(
            location_id="witch_interior",
            name="Inside the Witch's Hut",
            description="The cluttered, magical interior of the witch's home.",
            long_description="""The inside of the hut is much larger than the outside suggests - 
magic at work, no doubt. Every surface is covered with magical 
ingredients: jars of eyes, bottles of colored liquid, bundles of 
strange herbs, and things you can't even identify.

A massive cauldron bubbles over a fire that burns green, and the 
witch herself stirs it with a long wooden spoon. She's old - 
ancient even - but her eyes are sharp and knowing.

"Well, well," she cackles. "A visitor. How... unexpected. What 
brings you to my humble home, little mortal?"

Around her, dozens of cats watch you with glowing eyes.""",
            routes=[
                Route(1, "witch_hut", "Exit the hut", danger_level=0),
            ],
            creatures=[CreatureFactory.create_creature("witch")],
            items=[ItemFactory.create_item("greater healing potion"), ItemFactory.create_item("mana potion"),
                   ItemFactory.create_item("antidote")],
            features=["magical clutter", "bubbling cauldron", "watching cats", "powerful witch"],
            special_actions=["ask for help", "request potion", "offer trade", "attack"],
            ambient_sounds=["cauldron bubbling", "cats meowing", "witch humming"]
        )
        
        locations["witch_garden"] = Location(
            location_id="witch_garden",
            name="Witch's Garden",
            description="A garden of magical and poisonous plants.",
            long_description="""Behind the hut, the witch maintains a garden of the most dangerous 
and valuable plants in the forest. Nightshade grows next to 
mandrake, wolfsbane beside belladonna. Some plants whisper as you 
pass, and others reach out with grasping tendrils.

The witch clearly uses these for her potions. Taking some would be 
risky - she'll notice - but they could be invaluable.""",
            routes=[
                Route(1, "witch_hut", "Return to the front of the hut", danger_level=0),
            ],
            items=[ItemFactory.create_item("healing herb"), ItemFactory.create_item("mushroom")],
            features=["dangerous plants", "magical herbs", "whispering flora", "grasping vines"],
            ambient_sounds=["plants whispering", "magical humming"]
        )
        
        # ===================================================================
        # THORNY THICKET AREA
        # ===================================================================
        locations["thorny_thicket"] = Location(
            location_id="thorny_thicket",
            name="Thorny Thicket",
            description="A dense barrier of thorny bushes blocks your path.",
            long_description="""Massive thorny bushes form an almost impenetrable barrier. The thorns 
are as long as your finger and look sharp enough to pierce leather. 
Trying to push through would tear your clothes and skin to shreds.

But you can see something beyond the thicket - the ruins of what 
might be an old building, and what looks like a path leading to 
other parts of the forest.

There must be a way through, or around.""",
            routes=[
                Route(1, "clearing", "Return to the clearing", danger_level=0),
                Route(2, "thicket_path", "Search for a gap in the thorns", danger_level=2),
                Route(3, "cut_through", "Try to cut through with a blade", 
                      danger_level=3, requires_item="hunting knife"),
                Route(4, "burn_through", "Try to burn a path through", 
                      danger_level=2, requires_item="torch"),
            ],
            features=["massive thorns", "impenetrable barrier", "ruins beyond", "hidden path"],
            ambient_sounds=["wind through thorns", "rustling bushes"]
        )
        
        locations["thicket_path"] = Location(
            location_id="thicket_path",
            name="Hidden Path Through Thorns",
            description="A narrow path winds through the thorny barrier.",
            long_description="""You've found a narrow path that winds through the thorns - probably 
an animal trail, judging by the tracks. The thorns still grab at 
your clothes and scratch exposed skin, but it's passable if you're 
careful.

The path twists and turns, and in places you have to crawl beneath 
low-hanging branches covered in spikes. But eventually, you see 
light ahead - the other side.""",
            routes=[
                Route(1, "thorny_thicket", "Return through the path", danger_level=1),
                Route(2, "abandoned_village", "Continue to the other side", danger_level=1),
            ],
            features=["narrow path", "animal trail", "grasping thorns", "crawl spaces"],
            ambient_sounds=["cloth tearing", "thorns scraping"]
        )
        
        locations["cut_through"] = Location(
            location_id="cut_through",
            name="Cutting Through the Thorns",
            description="Hacking your way through the dense thorns.",
            long_description="""You cut and slash at the thorns, slowly carving a path through. 
It's exhausting work, and the thorns seem to grow back almost as 
fast as you cut them. Your blade dulls with each stroke.

But you're making progress. The ruins grow closer with each 
section you clear.""",
            routes=[
                Route(1, "thorny_thicket", "Give up and go back", danger_level=1),
                Route(2, "abandoned_village", "Push through to the ruins", danger_level=2),
            ],
            features=["cut thorns", "dulling blade", "slow progress"],
            ambient_sounds=["blade cutting", "thorns falling", "heavy breathing"]
        )
        
        locations["burn_through"] = Location(
            location_id="burn_through",
            name="Burning Through the Thorns",
            description="Using fire to clear a path through the thorns.",
            long_description="""The thorns are dry and burn quickly, creating a path through the 
thicket. Smoke fills the air, and you have to be careful not to 
let the fire spread too far - or burn yourself.

The heat is intense, and the smoke makes it hard to breathe, but 
it's effective. Soon you've cleared enough to pass through.""",
            routes=[
                Route(1, "thorny_thicket", "Return before the fire spreads", danger_level=1),
                Route(2, "abandoned_village", "Pass through the burned area", danger_level=1),
            ],
            features=["burning thorns", "smoke", "intense heat", "cleared path"],
            ambient_sounds=["fire crackling", "smoke hissing", "thorns burning"]
        )
        
        # ===================================================================
        # ABANDONED VILLAGE
        # ===================================================================
        locations["abandoned_village"] = Location(
            location_id="abandoned_village",
            name="Abandoned Village",
            description="The ruins of a village, long deserted.",
            long_description="""Beyond the thorns lies a village that was abandoned long ago. 
Cottages stand with collapsed roofs and empty windows. Weeds grow 
through the cobblestone streets. A dry fountain sits in the center 
of the village square.

Whatever drove the villagers away left everything behind - tools 
still hang in workshops, dishes still sit on tables. It's as if 
everyone simply vanished one day.

The silence here is oppressive. No birds sing, no insects buzz. 
The village feels... wrong.""",
            routes=[
                Route(1, "thicket_path", "Return through the thorns", danger_level=1),
                Route(2, "village_square", "Explore the village square", danger_level=1),
                Route(3, "old_church", "Enter the old church", danger_level=2),
                Route(4, "village_well", "Investigate the village well", danger_level=2),
                Route(5, "village_inn", "Enter the abandoned inn", danger_level=2),
                Route(6, "village_graveyard", "Visit the graveyard beyond the village", danger_level=3),
            ],
            items=[ItemFactory.create_item("cloth"), ItemFactory.create_item("wood")],
            features=["ruined cottages", "empty streets", "dry fountain", "abandoned tools"],
            ambient_sounds=["eerie silence", "wind through ruins", "creaking doors"],
            dangerous=True,
            danger_level=2
        )
        
        locations["village_square"] = Location(
            location_id="village_square",
            name="Village Square",
            description="The center of the abandoned village.",
            long_description="""The village square is dominated by a large dry fountain carved with 
images of people dancing and celebrating. At its center, a statue 
of a woman holds an empty basin that once spouted water.

Around the square, the largest buildings face inward - the inn, 
the church, the general store. All stand empty now, windows dark 
and doors hanging open.

On the fountain's edge, someone has scratched a message: "They 
came at night. We couldn't stop them. Run while you can." """,
            routes=[
                Route(1, "abandoned_village", "Return to the village entrance", danger_level=0),
                Route(2, "old_church", "Enter the church", danger_level=2),
                Route(3, "village_inn", "Enter the inn", danger_level=2),
                Route(4, "general_store", "Enter the general store", danger_level=1),
            ],
            items=[ItemFactory.create_item("gold coins")],
            features=["dry fountain", "carved statue", "scratched warning", "empty buildings"],
            ambient_sounds=["wind whistling", "doors creaking", "ominous silence"]
        )
        
        locations["general_store"] = Location(
            location_id="general_store",
            name="Abandoned General Store",
            description="A ransacked general store.",
            long_description="""The general store has been thoroughly looted. Shelves are knocked 
over, goods scattered across the floor. Whatever the villagers 
couldn't carry, they left behind in their desperate flight.

Still, some useful items remain among the debris. Tools, preserved 
food, and even some equipment that might help you survive.""",
            routes=[
                Route(1, "village_square", "Return to the square", danger_level=0),
            ],
            items=[ItemFactory.create_item("rope"), ItemFactory.create_item("dried meat"),
                   ItemFactory.create_item("lantern"), ItemFactory.create_item("shovel")],
            features=["overturned shelves", "scattered goods", "broken windows"],
            ambient_sounds=["items shifting", "floorboards creaking"]
        )
        
        locations["old_church"] = Location(
            location_id="old_church",
            name="Old Church",
            description="A small church with a wooden bell tower.",
            long_description="""The church is the best-preserved building in the village. Its heavy 
wooden doors still hang on their hinges, and most of the stained 
glass windows remain intact, though cracked.

Inside, pews face an altar carved with holy symbols. Behind the 
altar, a large book lies open to a page about protective wards 
against evil. The words are underlined multiple times, as if 
someone read them over and over seeking protection.

A stairway leads up to the bell tower.""",
            routes=[
                Route(1, "village_square", "Exit the church", danger_level=0),
                Route(2, "bell_tower", "Climb to the bell tower", danger_level=1),
                Route(3, "church_basement", "Descend to the basement", danger_level=2),
            ],
            items=[ItemFactory.create_item("spirit ward"), ItemFactory.create_item("healing potion")],
            features=["wooden pews", "holy altar", "stained glass", "protective texts"],
            ambient_sounds=["creaking wood", "wind through cracks", "distant bell"],
            rest_allowed=True
        )
        
        locations["bell_tower"] = Location(
            location_id="bell_tower",
            name="Church Bell Tower",
            description="The top of the church bell tower.",
            long_description="""From the bell tower, you can see the entire village laid out below, 
and beyond it, more of the forest. The bell itself hangs silent, 
its rope rotted away.

Someone used this as a lookout post - there are blankets and empty 
food containers up here, along with a spyglass. They must have 
watched for whatever drove the villagers away.

Through the spyglass, you can see far into the distance. To the 
north, you spot a tall stone tower rising above the trees.""",
            routes=[
                Route(1, "old_church", "Descend back to the church", danger_level=0),
            ],
            items=[ItemFactory.create_item("compass"), ItemFactory.create_item("feather")],
            features=["silent bell", "spyglass", "lookout post", "panoramic view"],
            ambient_sounds=["wind howling", "bell swaying", "distant sounds"]
        )
        
        locations["church_basement"] = Location(
            location_id="church_basement",
            name="Church Basement",
            description="A dark basement beneath the church.",
            long_description="""The basement was used for storage, but it's clear people took 
shelter here too. Makeshift beds line the walls, and barricades 
have been built against the door.

They were hiding from something. Something that scared them enough 
to abandon their village and take refuge in this cramped, dark space.

In one corner, you find a journal. The last entry is smeared with 
what looks like blood.""",
            routes=[
                Route(1, "old_church", "Return upstairs", danger_level=1),
            ],
            items=[ItemFactory.create_item("old journal"), ItemFactory.create_item("bandage"),
                   ItemFactory.create_item("dried meat")],
            features=["makeshift beds", "barricaded door", "bloody journal", "signs of panic"],
            dark=True,
            ambient_sounds=["dripping water", "your own breathing", "distant scratching"]
        )
        
        locations["village_well"] = Location(
            location_id="village_well",
            name="Village Well",
            description="An old stone well at the edge of the village.",
            long_description="""The well is deep and dark, its stones covered in moss. When you 
drop a pebble, you hear it splash far below - the water is still 
there, at least.

But something else is down there too. You can hear... movement. 
Scraping. Something alive in the depths of the well.

A rusty bucket hangs from the well's mechanism. You could lower 
yourself down, if you were brave - or foolish - enough.""",
            routes=[
                Route(1, "abandoned_village", "Step away from the well", danger_level=0),
                Route(2, "well_depths", "Descend into the well", 
                      danger_level=4, requires_item="rope"),
            ],
            items=[ItemFactory.create_item("fresh water")],
            features=["deep well", "mossy stones", "sounds from below", "rusty bucket"],
            water=True,
            ambient_sounds=["dripping water", "echoing depths", "something moving below"]
        )
        
        locations["well_depths"] = Location(
            location_id="well_depths",
            name="Well Depths",
            description="At the bottom of the village well.",
            long_description="""The well bottom is slick with algae and standing water. Your light 
reveals something horrifying - bones. Many bones. This well was 
used to dispose of bodies.

But some of those bodies aren't quite dead. Pale, twisted creatures 
drag themselves through the water - things that were once human but 
have been changed by their time in the dark.

In a small alcove, you spot something glinting - perhaps dropped 
by an earlier victim.""",
            routes=[
                Route(1, "village_well", "Climb back up", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("ghost"), CreatureFactory.create_creature("skeleton")],
            items=[ItemFactory.create_item("silver ore"), ItemFactory.create_item("gemstone")],
            features=["standing water", "scattered bones", "twisted creatures", "hidden alcove"],
            dark=True,
            water=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["water dripping", "bones shifting", "inhuman sounds"]
        )
        
        locations["village_inn"] = Location(
            location_id="village_inn",
            name="Abandoned Inn",
            description="The village inn, tables still set for meals never eaten.",
            long_description="""The inn is frozen in time. Tables are set with plates and cups, 
as if waiting for diners who never arrived. Behind the bar, bottles 
of wine and ale still line the shelves.

Upstairs, you can hear footsteps. Slow, dragging footsteps pacing 
back and forth, back and forth, endlessly.

A sign behind the bar reads: "Warm beds and hot meals." The 
irony is not lost on you.""",
            routes=[
                Route(1, "village_square", "Leave the inn", danger_level=0),
                Route(2, "inn_upstairs", "Go upstairs to investigate the footsteps", danger_level=3),
                Route(3, "inn_cellar", "Explore the wine cellar", danger_level=1),
            ],
            items=[ItemFactory.create_item("dried meat"), ItemFactory.create_item("gold coins")],
            features=["set tables", "bottles on shelves", "footsteps above", "abandoned meals"],
            ambient_sounds=["creaking floorboards", "pacing footsteps", "bottles clinking"],
            rest_allowed=True
        )
        
        locations["inn_upstairs"] = Location(
            location_id="inn_upstairs",
            name="Inn Upper Floor",
            description="The guest rooms of the inn.",
            long_description="""Multiple doors line the hallway, all standing open to reveal small, 
neat rooms with unmade beds. At the end of the hall, one door is 
closed. The footsteps come from behind it.

As you approach, the footsteps stop. The silence is somehow worse 
than the sound. You can feel something waiting on the other side 
of that door, listening for you just as you listen for it.

The doorknob slowly begins to turn...""",
            routes=[
                Route(1, "village_inn", "Flee back downstairs", danger_level=2),
                Route(2, "ghost_room", "Open the door", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("ghost")],
            features=["open doors", "unmade beds", "closed door", "turning doorknob"],
            dangerous=True,
            danger_level=3,
            ambient_sounds=["sudden silence", "doorknob turning", "breathing behind door"]
        )
        
        locations["ghost_room"] = Location(
            location_id="ghost_room",
            name="The Ghost's Room",
            description="A room occupied by a restless spirit.",
            long_description="""The room contains a ghost - the spirit of the innkeeper, trapped 
here, endlessly waiting for guests who will never come. It stares 
at you with hollow eyes, then speaks in a voice like wind through 
dead leaves.

"Finally... someone... I've been waiting so long... The thing in 
the forest... it took them all... but I remained... I must warn 
travelers... must warn..."

The ghost seems caught in a loop, unable to move on.""",
            routes=[
                Route(1, "inn_upstairs", "Leave the room", danger_level=1),
            ],
            creatures=[CreatureFactory.create_creature("ghost")],
            items=[ItemFactory.create_item("spirit essence"), ItemFactory.create_item("rusty key")],
            features=["trapped ghost", "endlessly waiting", "warning loop"],
            special_actions=["help ghost", "attack", "flee"],
            ambient_sounds=["ghostly whispers", "wind through walls", "endless waiting"]
        )
        
        locations["inn_cellar"] = Location(
            location_id="inn_cellar",
            name="Inn Wine Cellar",
            description="A cool cellar storing wine and supplies.",
            long_description="""The cellar is surprisingly well-stocked. Racks of wine bottles line 
the walls, and barrels of preserved food sit in neat rows. The 
innkeeper clearly prepared for a long winter... that never came.

Behind one of the wine racks, you notice something odd - fresh 
scratches on the floor, as if the rack has been moved recently. 
There might be a hidden room back there.""",
            routes=[
                Route(1, "village_inn", "Return upstairs", danger_level=0),
                Route(2, "secret_room", "Move the wine rack and investigate", danger_level=1),
            ],
            items=[ItemFactory.create_item("dried meat"), ItemFactory.create_item("traveler's ration")],
            features=["wine racks", "food barrels", "scratched floor", "hidden room"],
            ambient_sounds=["your footsteps", "bottles clinking"]
        )
        
        locations["secret_room"] = Location(
            location_id="secret_room",
            name="Hidden Room",
            description="A secret room behind the wine cellar.",
            long_description="""Behind the rack is a small hidden room - a smuggler's cache, or 
perhaps the innkeeper's personal treasure room. Either way, it's 
filled with valuable items.

Gold coins sit in a chest, along with jewelry and other precious 
items. There's also equipment that looks like it belonged to 
adventurers who stayed at the inn... and never checked out.""",
            routes=[
                Route(1, "inn_cellar", "Return to the cellar", danger_level=0),
            ],
            items=[ItemFactory.create_item("gold coins"), ItemFactory.create_item("gold coins"),
                   ItemFactory.create_item("chainmail"), ItemFactory.create_item("iron sword")],
            features=["treasure chest", "valuable items", "adventurer equipment"],
            ambient_sounds=["coins clinking", "your breathing"]
        )
        
        locations["village_graveyard"] = Location(
            location_id="village_graveyard",
            name="Village Graveyard",
            description="A small graveyard behind the church.",
            long_description="""Stone markers stand in neat rows, most so weathered the names are 
illegible. This graveyard served the village for generations, 
peacefully housing its dead.

But now the peace is shattered. Many graves have been disturbed - 
dug up from below, not above. Empty graves gape open like wounds 
in the earth.

Whatever drove the villagers away also raised their dead.""",
            routes=[
                Route(1, "abandoned_village", "Return to the village", danger_level=2),
                Route(2, "crypt_entrance", "Enter the family crypt at the back", danger_level=3),
                Route(3, "fresh_graves", "Investigate the recently disturbed graves", danger_level=2),
            ],
            creatures=[CreatureFactory.create_creature("skeleton"), CreatureFactory.create_creature("skeleton")],
            features=["weathered markers", "disturbed graves", "family crypt", "empty graves"],
            dangerous=True,
            danger_level=3,
            ambient_sounds=["wind through graves", "distant moaning", "earth shifting"]
        )
        
        locations["fresh_graves"] = Location(
            location_id="fresh_graves",
            name="Disturbed Graves",
            description="Graves that have been dug open from below.",
            long_description="""The graves have been opened from below, the coffins smashed outward. 
Whatever was buried here clawed its way out and wandered off into 
the forest - or perhaps into the village itself.

Among the debris, you find some items that were buried with the 
dead. Grave robbing is distasteful, but survival takes precedence 
over decorum.""",
            routes=[
                Route(1, "village_graveyard", "Return to the main graveyard", danger_level=1),
            ],
            items=[ItemFactory.create_item("gold coins"), ItemFactory.create_item("silver dagger")],
            features=["opened graves", "smashed coffins", "burial goods"],
            ambient_sounds=["wind through broken coffins", "earth crumbling"]
        )
        
        locations["crypt_entrance"] = Location(
            location_id="crypt_entrance",
            name="Family Crypt",
            description="The entrance to an old family crypt.",
            long_description="""A stone building built into a hillside, serves as the final resting place 
for the village's founding family. Heavy iron doors stand closed, 
sealed with a rusty lock.

Through cracks in the door, you can see faint light flickering - 
candlelight or perhaps something more sinister. Whatever is inside, 
it's not entirely abandoned.""",
            routes=[
                Route(1, "village_graveyard", "Return to the graveyard", danger_level=1),
                Route(2, "crypt_interior", "Pick the lock and enter", 
                      danger_level=4, requires_skill=(SkillType.LOCKPICKING, 3)),
                Route(3, "crypt_interior", "Force the doors open", danger_level=4),
            ],
            features=["stone building", "iron doors", "rusty lock", "flickering light"],
            dark=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["wind howling", "chains rattling", "something moving inside"]
        )
        
        locations["crypt_interior"] = Location(
            location_id="crypt_interior",
            name="Inside the Crypt",
            description="The dark interior of the family crypt.",
            long_description="""Candles line the walls, their flames guttering in an unfelt wind. 
Stone sarcophagi stand in neat rows, each carved with the name and 
likeness of a family member long dead.

At the far end of the crypt, on a raised platform, stands the 
largest sarcophagus - the family patriarch. And sitting atop it, 
reading from an ancient tome by candlelight, is a figure in dark 
robes.

It looks up as you enter. Its face is hidden beneath a deep hood, 
but you can feel its gaze upon you. "An intruder," it says in a 
voice like grinding stone. "Or perhaps... a sacrifice?""",
            routes=[
                Route(1, "crypt_entrance", "Flee back outside", danger_level=3),
                Route(2, "necromancer_battle", "Confront the figure", danger_level=5),
            ],
            creatures=[CreatureFactory.create_creature("skeleton"), CreatureFactory.create_creature("skeleton")],
            items=[ItemFactory.create_item("crypt key")],
            features=["guttering candles", "stone sarcophagi", "robed figure", "ancient tome"],
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["pages turning", "magical whispers", "stone grinding"]
        )
        
        locations["necromancer_battle"] = Location(
            location_id="necromancer_battle",
            name="Confronting the Necromancer",
            description="Face to face with a dark sorcerer.",
            long_description="""The necromancer rises, dark energy crackling around its hands. This 
is what drove the villagers away - this creature of death and dark 
magic, who raised their dead to serve it.

"You cannot stop what has already begun," it hisses. "The forest 
belongs to darkness now. You will join my army, one way or another."

Around you, the sarcophagi begin to open. The dead are rising.""",
            routes=[
                Route(1, "crypt_interior", "Try to escape", danger_level=4),
            ],
            creatures=[CreatureFactory.create_creature("wraith"), CreatureFactory.create_creature("skeleton"),
                      CreatureFactory.create_creature("skeleton"), CreatureFactory.create_creature("ghost")],
            items=[ItemFactory.create_item("enchanted staff"), ItemFactory.create_item("shadow essence"),
                   ItemFactory.create_item("gold coins"), ItemFactory.create_item("master key")],
            features=["necromancer", "rising dead", "crackling dark energy", "opening sarcophagi"],
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["magical crackling", "stone lids sliding", "necromancer laughing"]
        )
        
        # ===================================================================
        # DENSE FOREST AREA
        # ===================================================================
        locations["dense_forest"] = Location(
            location_id="dense_forest",
            name="Dense Forest",
            description="Trees grow so close together here that movement is difficult.",
            long_description="""The trees here grow unnaturally close, their trunks almost touching. 
Moving between them requires squeezing through narrow gaps and 
pushing aside thick undergrowth. Progress is slow and exhausting.

The canopy overhead is so dense that only scattered beams of light 
reach the forest floor. Strange fungi grow on the bark, glowing 
faintly with bioluminescence.

Animal sounds echo through the trees - howls, growls, and stranger 
things. This is wild territory.""",
            routes=[
                Route(1, "clearing", "Fight your way back to the clearing", danger_level=2),
                Route(2, "hunter_camp", "Follow game trails to a campsite", danger_level=1),
                Route(3, "bear_cave", "Investigate a large cave entrance", danger_level=4),
                Route(4, "tree_maze", "Navigate deeper into the dense trees", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("wolf")],
            items=[ItemFactory.create_item("wood"), ItemFactory.create_item("mushroom")],
            features=["closely-packed trees", "thick undergrowth", "glowing fungi", "animal sounds"],
            ambient_sounds=["branches creaking", "animals calling", "leaves rustling"],
            dangerous=True,
            danger_level=2
        )
        
        locations["hunter_camp"] = Location(
            location_id="hunter_camp",
            name="Hunter's Camp",
            description="A small camp used by hunters.",
            long_description="""Someone has made a camp here - a circle of stones for a fire pit, 
a crude shelter made of branches and hides, and racks for drying 
meat. The camp looks recently used, though no one is here now.

Traps and snares lie scattered about, along with hunting equipment. 
Whoever camps here is skilled at surviving in the forest.

A note is pinned to a tree: "Gone to check the northern traps. 
Back by nightfall. - Marcus.""",
            routes=[
                Route(1, "dense_forest", "Return to the dense forest", danger_level=1),
                Route(2, "northern_traps", "Follow the trail to the northern traps", danger_level=2),
            ],
            items=[ItemFactory.create_item("hunting bow"), ItemFactory.create_item("dried meat"),
                   ItemFactory.create_item("rope"), ItemFactory.create_item("hunting knife")],
            features=["fire pit", "crude shelter", "drying racks", "hunting equipment"],
            ambient_sounds=["fire crackling", "wind in trees"],
            rest_allowed=True,
            save_point=True
        )
        
        locations["northern_traps"] = Location(
            location_id="northern_traps",
            name="Trap Line",
            description="A line of traps set for game.",
            long_description="""A series of snares and deadfall traps stretches through the forest. 
Most are empty, but one has caught something - a rabbit, already dead.

Further along the trap line, you find the hunter. He's pinned beneath 
a fallen tree, his leg twisted at an unnatural angle. He's conscious 
but in obvious pain.

"Help... me..." he gasps. "Bear... knocked the tree... onto me..."

In the distance, you hear a deep growl. The bear is still nearby.""",
            routes=[
                Route(1, "hunter_camp", "Return to the camp", danger_level=2),
                Route(2, "help_hunter", "Try to help the trapped hunter", danger_level=0),
            ],
            creatures=[CreatureFactory.create_creature("bear")],
            items=[ItemFactory.create_item("dried meat"), ItemFactory.create_item("healing herb")],
            features=["trap line", "trapped hunter", "fallen tree", "nearby bear"],
            dangerous=True,
            danger_level=3,
            special_actions=["help hunter", "ignore hunter", "steal from hunter"],
            ambient_sounds=["hunter groaning", "distant growling", "leaves rustling"]
        )
        
        locations["help_hunter"] = Location(
            location_id="help_hunter",
            name="Helping the Hunter",
            description="Attempting to free the trapped hunter.",
            long_description="""You work to lift the tree off the hunter's leg. It's heavy, and 
he cries out in pain as you shift it. But slowly, carefully, you 
manage to free him.

He looks up at you with gratitude. "Thank you... I thought I was 
done for. The bear... it went crazy, attacked me out of nowhere. 
Not normal bear behavior."

He fumbles at his belt. "Here... take this. You saved my life. 
And... watch out for that bear. Something's wrong with it."

The growling grows louder. The bear is returning.""",
            routes=[
                Route(1, "northern_traps", "Get ready for the bear", danger_level=3),
            ],
            items=[ItemFactory.create_item("lucky charm"), ItemFactory.create_item("gold coins")],
            features=["grateful hunter", "lifted tree", "approaching bear"],
            dangerous=True,
            danger_level=4,
            ambient_sounds=["hunter breathing", "growling getting closer", "breaking branches"]
        )
        
        locations["bear_cave"] = Location(
            location_id="bear_cave",
            name="Bear's Cave",
            description="A large cave that serves as a bear's den.",
            long_description="""The cave reeks of animal musk and old kills. Bones are scattered 
across the floor - deer, rabbits, and... human. This bear has been 
eating people.

Deep in the cave, you can see the bear sleeping on a pile of leaves 
and moss. It's massive, even by bear standards, with matted fur and 
scars covering its body.

But there's something else - a strange growth on its neck, pulsing 
with dark energy. This bear has been corrupted by the same force 
that affects other parts of the forest.

You could try to sneak past, or end the threat now.""",
            routes=[
                Route(1, "dense_forest", "Quietly leave the cave", danger_level=2),
                Route(2, "bear_fight", "Attack while it sleeps", danger_level=4),
                Route(3, "cave_depths", "Sneak past to the deeper cave", 
                      danger_level=3, requires_skill=(SkillType.STEALTH, 4)),
            ],
            creatures=[CreatureFactory.create_creature("bear")],
            items=[ItemFactory.create_item("bear claw")],
            features=["animal musk", "bone pile", "sleeping bear", "dark growth"],
            dark=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["bear breathing", "bones shifting", "dripping water"]
        )
        
        locations["bear_fight"] = Location(
            location_id="bear_fight",
            name="Fighting the Corrupted Bear",
            description="Battle with a bear twisted by dark magic.",
            long_description="""The bear wakes with a roar that shakes the cave walls. But this 
is no normal bear - the corruption has made it stronger, faster, 
and filled with unnatural rage.

It fights with inhuman ferocity, seeming to feel no pain. The dark 
growth on its neck pulses with each attack, driving it to greater 
violence.

You must destroy both the bear and the corruption within it.""",
            routes=[
                Route(1, "bear_cave", "Try to flee", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("bear")],
            items=[ItemFactory.create_item("bear claw"), ItemFactory.create_item("shadow essence"),
                   ItemFactory.create_item("gold nugget")],
            features=["enraged bear", "pulsing corruption", "shaking cave"],
            dangerous=True,
            danger_level=5,
            ambient_sounds=["bear roaring", "claws scraping", "magical pulsing"]
        )
        
        locations["cave_depths"] = Location(
            location_id="cave_depths",
            name="Deep Cave",
            description="A narrow passage leading deeper into the mountain.",
            long_description="""Past the bear's den, the cave continues deeper into the mountain. 
The passage narrows until you have to crawl, then opens into a 
larger chamber.

This chamber is not natural - it's been carved by intelligent hands. 
Ancient dwarven runes cover the walls, and the floor is perfectly 
level. This was once part of a larger complex.

An old mining cart sits on rusted rails, and tools lie scattered 
about. The dwarves abandoned this place long ago.""",
            routes=[
                Route(1, "bear_cave", "Return to the bear's cave", danger_level=2),
                Route(2, "mining_tunnels", "Follow the rails deeper", danger_level=3),
            ],
            items=[ItemFactory.create_item("iron ore"), ItemFactory.create_item("stone"),
                   ItemFactory.create_item("old journal")],
            features=["dwarven runes", "mining cart", "abandoned tools", "carved walls"],
            dark=True,
            ambient_sounds=["water dripping", "metal creaking", "distant echoes"]
        )
        
        locations["mining_tunnels"] = Location(
            location_id="mining_tunnels",
            name="Old Mining Tunnels",
            description="Ancient dwarven mining tunnels.",
            long_description="""The tunnels stretch in multiple directions, a maze of passages 
carved centuries ago. Support beams hold up the ceiling, though 
many have rotted and collapsed.

Signs of mining are everywhere - ore carts, tools, and veins of 
precious metals still visible in the walls. The dwarves must have 
abandoned this place suddenly, leaving everything behind.

You can hear goblin voices echoing through the tunnels. They've 
made their home here in the abandoned mines.""",
            routes=[
                Route(1, "cave_depths", "Return to the cave entrance", danger_level=2),
                Route(2, "goblin_warren", "Follow the goblin voices", danger_level=4),
                Route(3, "treasure_chamber", "Find a way to the sealed chamber", 
                      danger_level=3, requires_item="master key"),
            ],
            creatures=[CreatureFactory.create_creature("goblin")],
            items=[ItemFactory.create_item("iron ore"), ItemFactory.create_item("silver ore")],
            features=["maze of tunnels", "rotted supports", "ore veins", "goblin presence"],
            dark=True,
            dangerous=True,
            danger_level=3,
            ambient_sounds=["goblin chatter", "tunnels settling", "cart wheels squeaking"]
        )
        
        locations["goblin_warren"] = Location(
            location_id="goblin_warren",
            name="Goblin Warren",
            description="The goblins' living quarters in the old mines.",
            long_description="""The goblins have transformed part of the mines into their home. 
Crude shelters made of scrap wood and cloth fill a large chamber, 
and cooking fires burn in metal barrels.

Dozens of goblins move about their daily business - crafting crude 
weapons, cooking suspicious-looking meat, arguing amongst themselves. 
At the center, on a throne made of junk, sits their leader - a 
larger goblin covered in crude jewelry and wielding a notched blade.

They haven't noticed you yet. You could try to sneak through, fight 
your way out, or perhaps... negotiate?""",
            routes=[
                Route(1, "mining_tunnels", "Sneak back to the tunnels", danger_level=2),
                Route(2, "goblin_leader", "Approach the leader", danger_level=4),
                Route(3, "slave_pens", "Investigate the cages at the back", danger_level=2),
            ],
            creatures=[CreatureFactory.create_creature("goblin"), CreatureFactory.create_creature("goblin"),
                      CreatureFactory.create_creature("goblin scout"), CreatureFactory.create_creature("goblin shaman")],
            items=[ItemFactory.create_item("rusty knife"), ItemFactory.create_item("gold coins")],
            features=["crude shelters", "cooking fires", "junk throne", "goblin community"],
            dark=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["goblin chatter", "fires crackling", "arguing", "metal clanging"]
        )
        
        locations["goblin_leader"] = Location(
            location_id="goblin_leader",
            name="Before the Goblin Chief",
            description="Standing before the goblin leader.",
            long_description="""The goblin chief regards you with cunning eyes. Unlike the others, 
this one is intelligent - dangerous not just because of strength, 
but because it can think.

"Well, well," it says in surprisingly clear Common. "A human. Here. 
In OUR mines. You brave, or stupid?"

It leans forward on its throne. "You kill many goblins to get here? 
Or you sneak good? Either way, Chief impressed. Maybe Chief no kill 
you... if you do something for Chief first."

The other goblins watch eagerly, waiting to see if they'll get to 
fight you.""",
            routes=[
                Route(1, "goblin_warren", "Back away from the chief", danger_level=2),
            ],
            creatures=[CreatureFactory.create_creature("goblin"), CreatureFactory.create_creature("goblin")],
            items=[ItemFactory.create_item("golden key"), ItemFactory.create_item("gold coins")],
            features=["cunning chief", "junk throne", "watching goblins"],
            dangerous=True,
            danger_level=4,
            special_actions=["accept quest", "refuse", "attack", "bribe"],
            ambient_sounds=["chief's breathing", "goblins muttering", "throne creaking"]
        )
        
        locations["slave_pens"] = Location(
            location_id="slave_pens",
            name="Goblin Slave Pens",
            description="Crude cages holding prisoners.",
            long_description="""Several makeshift cages hold prisoners - mostly humans, but also 
a dwarf and what looks like an elf. They're in poor condition, 
thin and covered in bruises.

One prisoner, a young woman in torn noble's clothing, reaches 
through the bars. "Please," she whispers. "Help us. They're going 
to... to eat us. One by one. The keys are with the guard."

A goblin guard snores nearby, keys dangling from its belt.""",
            routes=[
                Route(1, "goblin_warren", "Return to the main warren", danger_level=1),
            ],
            creatures=[CreatureFactory.create_creature("goblin scout")],
            items=[ItemFactory.create_item("rusty key")],
            features=["crude cages", "starving prisoners", "sleeping guard", "keys"],
            special_actions=["free prisoners", "steal keys", "ignore prisoners"],
            ambient_sounds=["prisoners whimpering", "guard snoring", "chains rattling"]
        )
        
        locations["treasure_chamber"] = Location(
            location_id="treasure_chamber",
            name="Dwarven Treasure Vault",
            description="An ancient dwarven treasure chamber.",
            long_description="""The sealed door opens to reveal a treasure vault carved from solid 
stone. Gold and silver coins fill chests, weapons and armor line 
the walls, and precious gems glitter in every color imaginable.

This is the wealth of a dwarven clan, abandoned when they left 
these mines. The goblins never found this room - the dwarven locks 
were too sophisticated for them.

At the center of the vault, on a pedestal, rests a magnificent 
warhammer that glows with inner light. This is a weapon of legend.""",
            routes=[
                Route(1, "mining_tunnels", "Exit with your findings", danger_level=2),
            ],
            items=[ItemFactory.create_item("gold coins"), ItemFactory.create_item("gold coins"),
                   ItemFactory.create_item("gold coins"), ItemFactory.create_item("gemstone"),
                   ItemFactory.create_item("gemstone"), ItemFactory.create_item("ancient artifact"),
                   ItemFactory.create_item("chainmail"), ItemFactory.create_item("iron sword")],
            features=["treasure chests", "weapon racks", "glowing warhammer", "precious gems"],
            ambient_sounds=["coins shifting", "magical humming", "your amazed breathing"]
        )
        
        locations["tree_maze"] = Location(
            location_id="tree_maze",
            name="Maze of Trees",
            description="Lost in a confusing maze of identical trees.",
            long_description="""The trees here all look exactly the same, creating a disorienting 
maze. You've lost all sense of direction, and every path looks 
identical to the last.

You could wander here for days without finding your way out. Strange 
markings on some trees might indicate a path... or might be a trap 
to lure the lost deeper into the maze.

In the distance, you hear singing - a beautiful, haunting melody.""",
            routes=[
                Route(1, "dense_forest", "Try to retrace your steps", danger_level=2),
                Route(2, "maze_center", "Follow the singing", danger_level=3),
                Route(3, "maze_exit", "Follow the tree markings", 
                      danger_level=2, requires_skill=(SkillType.SURVIVAL, 3)),
            ],
            features=["identical trees", "tree markings", "disorientation", "distant singing"],
            ambient_sounds=["haunting melody", "wind through trees", "your footsteps"],
            dangerous=True,
            danger_level=3
        )
        
        locations["maze_center"] = Location(
            location_id="maze_center",
            name="Center of the Maze",
            description="A clearing at the heart of the tree maze.",
            long_description="""At the center of the maze is a small clearing with a pool of crystal-
clear water. Sitting beside the pool is the source of the singing - 
a beautiful woman with long, flowing hair.

But as you approach, you see the truth. From the waist down, she's 
not human but deer. This is a dryad, a spirit of the forest, and 
her song has the power to entrance.

She stops singing and looks at you with ancient eyes. "Few find 
their way to my sanctuary. You must be either very clever or very 
lost. Which is it, mortal?""",
            routes=[
                Route(1, "tree_maze", "Leave the clearing", danger_level=2),
            ],
            creatures=[CreatureFactory.create_creature("tree spirit")],
            items=[ItemFactory.create_item("nature's embrace"), ItemFactory.create_item("healing herb")],
            features=["crystal pool", "dryad", "forest spirit", "enchanting presence"],
            special_actions=["speak with dryad", "attack", "drink from pool"],
            ambient_sounds=["water trickling", "gentle humming", "forest breathing"]
        )
        
        locations["maze_exit"] = Location(
            location_id="maze_exit",
            name="Exit from the Maze",
            description="Finding your way out of the tree maze.",
            long_description="""By carefully following the markings and using your survival instincts, 
you've navigated through the maze. The trees begin to thin, and you 
can see clearer paths ahead.

You've made it through - a test of patience and skill.""",
            routes=[
                Route(1, "dense_forest", "Return to the dense forest", danger_level=1),
                Route(2, "mountain_path", "Continue west toward the mountains", danger_level=2),
            ],
            items=[ItemFactory.create_item("compass")],
            features=["thinning trees", "clearer paths", "sense of accomplishment"]
        )
        
        # ===================================================================
        # ANIMAL DEN AREA
        # ===================================================================
        locations["animal_den"] = Location(
            location_id="animal_den",
            name="Animal Den",
            description="A den where various forest animals seek shelter.",
            long_description="""The den is a natural hollow beneath the roots of a massive tree. 
Various animals have used it over the years - you can see different 
types of fur, feathers, and tracks.

Currently, it's home to a family of foxes. The mother watches you 
warily, her kits huddled behind her. She growls low in warning but 
doesn't attack - just protecting her young.

Deeper in the den, you notice something glinting.""",
            routes=[
                Route(1, "stream_south", "Leave the animals in peace", danger_level=0),
                Route(2, "den_depths", "Carefully explore deeper", 
                      danger_level=1, requires_skill=(SkillType.STEALTH, 2)),
            ],
            features=["tree root ceiling", "fox family", "various animal signs", "protective mother"],
            ambient_sounds=["fox growling", "kits whimpering", "earth smells"]
        )
        
        locations["den_depths"] = Location(
            location_id="den_depths",
            name="Back of the Den",
            description="The deeper section of the animal den.",
            long_description="""At the back of the den, you find what the foxes have been using as 
toys - a leather pouch, probably dropped by a traveler long ago. 
The foxes have chewed on it but haven't managed to open it.

Inside, you find some useful items, preserved by the leather.""",
            routes=[
                Route(1, "animal_den", "Return to the den entrance", danger_level=0),
            ],
            items=[ItemFactory.create_item("gold coins"), ItemFactory.create_item("lockpick"),
                   ItemFactory.create_item("map fragment")],
            features=["leather pouch", "fox toys", "earth walls"],
            ambient_sounds=["foxes moving", "earth sounds"]
        )
        
        locations["stream_falls"] = Location(
            location_id="stream_falls",
            name="Stream Falls",
            description="Where the stream drops down a rocky slope.",
            long_description="""The stream cascades down a series of rocky shelves here, creating 
small waterfalls and pools. It's not as dramatic as the main 
waterfall, but it's beautiful in its own way.

The rocks are slick with spray, making this a treacherous area. 
One wrong step could send you tumbling down with the water.

At the bottom, you can see the stream continues into a dark area - 
what might be a swamp.""",
            routes=[
                Route(1, "stream_bend", "Climb back up the slope", danger_level=2),
                Route(2, "swamp_edge", "Carefully descend following the stream", danger_level=3),
            ],
            features=["cascading water", "slick rocks", "multiple pools", "spray"],
            water=True,
            climbable=True,
            dangerous=True,
            danger_level=2,
            ambient_sounds=["water falling", "rocks tumbling", "spray hissing"]
        )
        
        # ===================================================================
        # SWAMP AREA
        # ===================================================================
        locations["swamp_edge"] = Location(
            location_id="swamp_edge",
            name="Edge of the Swamp",
            description="The forest gives way to a dark, murky swamp.",
            long_description="""The solid ground ends here, replaced by muddy earth and standing 
water. Trees grow twisted and gnarled, their roots visible above 
the murky water. Thick fog hangs low over everything, and the air 
smells of decay and stagnant water.

Strange sounds echo across the swamp - splashing, croaking, and 
things you can't identify. Lights flicker in the distance - will-o'-
wisps that lure travelers to their doom.

This is treacherous territory. One wrong step could plunge you into 
deep water or sucking mud.""",
            routes=[
                Route(1, "mist_clearing", "Return to the forest", danger_level=1),
                Route(2, "stream_falls", "Climb up to the stream falls", danger_level=2),
                Route(3, "swamp_path", "Follow the narrow path into the swamp", danger_level=3),
                Route(4, "will_o_wisp", "Follow the distant lights", danger_level=4),
            ],
            features=["murky water", "twisted trees", "thick fog", "flickering lights"],
            water=True,
            dangerous=True,
            danger_level=3,
            ambient_sounds=["croaking frogs", "bubbling mud", "mysterious splashing", "eerie silence"]
        )
        
        locations["swamp_path"] = Location(
            location_id="swamp_path",
            name="Swamp Path",
            description="A narrow, treacherous path through the swamp.",
            long_description="""The path is barely more than a series of slightly firmer mud patches 
and half-submerged logs. You must step carefully, testing each spot 
before putting your full weight on it.

The water on either side is dark and still, its depth impossible to 
judge. Things move beneath the surface - you can see ripples and 
occasionally a scaled back breaking the water.

Ahead, you spot what looks like a small island with a hut built on 
stilts.""",
            routes=[
                Route(1, "swamp_edge", "Return to solid ground", danger_level=2),
                Route(2, "swamp_hut", "Continue to the island and hut", danger_level=2),
                Route(3, "deep_swamp", "Wade into the deeper water", 
                      danger_level=4, requires_skill=(SkillType.SWIMMING, 3)),
            ],
            creatures=[CreatureFactory.create_creature("swamp creature")],
            features=["muddy path", "half-submerged logs", "dark water", "things below surface"],
            water=True,
            dangerous=True,
            danger_level=3,
            ambient_sounds=["sucking mud", "water lapping", "creature sounds"]
        )
        
        locations["swamp_hut"] = Location(
            location_id="swamp_hut",
            name="Swamp Hut",
            description="A hut built on stilts above the swamp water.",
            long_description="""The hut is crude but sturdy, built to survive the harsh swamp 
environment. Smoke rises from a crooked chimney, and a small boat 
is tied to the stilts below.

Someone lives here - someone who has adapted to survive in this 
hostile place. As you approach, an old woman emerges from the hut, 
eyeing you suspiciously.

"Well now," she croaks. "Rare to see a traveler out here. Most who 
come to the swamp don't leave. What brings you to my door?""",
            routes=[
                Route(1, "swamp_path", "Leave the island", danger_level=1),
                Route(2, "hut_interior", "Enter the hut", danger_level=0),
                Route(3, "swamp_boat", "Take the boat", danger_level=2),
            ],
            creatures=[CreatureFactory.create_creature("witch")],
            items=[ItemFactory.create_item("antidote")],
            features=["stilted hut", "smoking chimney", "tied boat", "suspicious resident"],
            ambient_sounds=["wood creaking", "water below", "old woman muttering"]
        )
        
        locations["hut_interior"] = Location(
            location_id="hut_interior",
            name="Inside the Swamp Hut",
            description="The interior of the swamp dweller's hut.",
            long_description="""The hut is filled with herbs, preserved creatures in jars, and 
various tools for surviving the swamp. The old woman is clearly 
some kind of herbalist or wise woman.

"Aye, I know these swamps better than anyone," she says. "Been 
living here forty years. I know the safe paths, the safe plants, 
and the things best avoided. You want to get through alive? You'll 
need my help."

She gestures to a chair. "Sit. We'll talk business."
""",
            routes=[
                Route(1, "swamp_hut", "Exit the hut", danger_level=0),
            ],
            creatures=[CreatureFactory.create_creature("witch")],
            items=[ItemFactory.create_item("antidote"), ItemFactory.create_item("healing potion"),
                   ItemFactory.create_item("map fragment")],
            features=["herb bundles", "preserved creatures", "survival tools", "wise woman"],
            special_actions=["ask for help", "trade", "ask about swamp"],
            shop_available=True,
            ambient_sounds=["fire crackling", "jars clinking", "swamp sounds outside"]
        )
        
        locations["swamp_boat"] = Location(
            location_id="swamp_boat",
            name="Swamp Boat",
            description="A small boat for navigating the swamp waters.",
            long_description="""The boat is a simple flat-bottomed craft, perfect for the shallow 
swamp waters. A long pole rests inside for pushing through the muck.

From here, you can reach parts of the swamp that would be impossible 
to access on foot. The dark water stretches in every direction, 
broken only by occasional islands and the twisted trunks of 
half-drowned trees.""",
            routes=[
                Route(1, "swamp_hut", "Return to the hut", danger_level=0),
                Route(2, "deep_swamp", "Pole into the deeper swamp", danger_level=3),
                Route(3, "sunken_ruins", "Navigate toward the stone ruins you can see", danger_level=4),
                Route(4, "will_o_wisp", "Follow the flickering lights", danger_level=4),
            ],
            features=["flat-bottomed boat", "push pole", "murky water", "distant islands"],
            water=True,
            ambient_sounds=["water lapping", "pole splashing", "distant croaking"]
        )
        
        locations["deep_swamp"] = Location(
            location_id="deep_swamp",
            name="Deep Swamp",
            description="The heart of the treacherous swamp.",
            long_description="""Here, the swamp is at its worst. The water is chest-deep in places, 
the mud tries to suck you down with every step, and the fog is so 
thick you can barely see your hand in front of your face.

Something large moves through the water nearby - you can hear it 
but not see it. The splashing is too heavy to be anything small.

This is a dangerous place. The swamp claims many victims.""",
            routes=[
                Route(1, "swamp_path", "Try to find your way back", danger_level=3),
                Route(2, "swamp_boat", "Return to the boat", danger_level=2),
                Route(3, "sunken_ruins", "Push toward the stone structures ahead", danger_level=4),
            ],
            creatures=[CreatureFactory.create_creature("swamp creature"), 
                      CreatureFactory.create_creature("swamp creature")],
            items=[ItemFactory.create_item("gold coins")],
            features=["deep water", "sucking mud", "thick fog", "unseen creatures"],
            water=True,
            swimmable=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["heavy splashing", "bubbling mud", "creature sounds", "your labored breathing"]
        )
        
        locations["will_o_wisp"] = Location(
            location_id="will_o_wisp",
            name="Will-o'-Wisp Lights",
            description="Following the mysterious lights deeper into the swamp.",
            long_description="""The lights dance just ahead of you, always staying out of reach. 
They're beautiful - pale blue and green, flickering like candle 
flames but moving with purpose.

You know the legends. Will-o'-wisps lead travelers to their doom, 
luring them into deep water or quicksand. But these lights seem 
to be leading you somewhere specific...

The lights converge on a small island where something ancient stands.""",
            routes=[
                Route(1, "swamp_edge", "Try to escape the lights", danger_level=3),
                Route(2, "ancient_shrine", "Follow the lights to the island", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("ghost")],
            features=["dancing lights", "will-o'-wisps", "specific destination", "ancient island"],
            dangerous=True,
            danger_level=4,
            ambient_sounds=["ethereal humming", "water splashing", "lights flickering"]
        )
        
        locations["ancient_shrine"] = Location(
            location_id="ancient_shrine",
            name="Ancient Shrine",
            description="A crumbling shrine on a small swamp island.",
            long_description="""The will-o'-wisps have led you to an ancient shrine, half-sunken 
into the swamp. Stone walls covered in moss and lichen surround 
a central altar where the lights now gather and merge.

The altar is carved with symbols of death and rebirth - this was 
a place where the ancient people honored the cycle of life. The 
will-o'-wisps, you realize, are the spirits of those who died 
here, still performing their eternal rituals.

On the altar rests an object that pulses with spiritual energy.""",
            routes=[
                Route(1, "will_o_wisp", "Leave the shrine", danger_level=2),
            ],
            items=[ItemFactory.create_item("spirit essence"), ItemFactory.create_item("spirit ward"),
                   ItemFactory.create_item("ancient amulet")],
            features=["half-sunken shrine", "merging lights", "death symbols", "spiritual energy"],
            special_actions=["pray", "take artifact", "speak with spirits"],
            ambient_sounds=["spiritual humming", "whispered prayers", "ancient echoes"]
        )
        
        locations["sunken_ruins"] = Location(
            location_id="sunken_ruins",
            name="Sunken Ruins",
            description="Ancient ruins slowly sinking into the swamp.",
            long_description="""Once, this was a great building - a temple or palace of some 
forgotten civilization. Now it sinks slowly into the swamp, only 
its upper floors remaining above water.

The architecture is strange and unsettling, with proportions that 
seem wrong to human eyes. Carvings depict beings that might be 
gods or might be monsters.

Something valuable glints in the murky water below, and there 
appears to be a way into the submerged lower levels.""",
            routes=[
                Route(1, "deep_swamp", "Return to the deep swamp", danger_level=3),
                Route(2, "swamp_boat", "Return to the boat", danger_level=2),
                Route(3, "ruins_upper", "Explore the upper ruins", danger_level=3),
                Route(4, "ruins_submerged", "Dive to the submerged levels", 
                      danger_level=5, requires_skill=(SkillType.SWIMMING, 4)),
            ],
            features=["sinking architecture", "strange carvings", "submerged levels", "glinting treasure"],
            water=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["water dripping", "stone settling", "something moving below"]
        )
        
        locations["ruins_upper"] = Location(
            location_id="ruins_upper",
            name="Upper Ruins",
            description="The upper floors of the sunken ruins.",
            long_description="""The upper floors are damaged but passable. You pick your way through 
collapsed hallways and crumbling chambers, finding remnants of a 
civilization that vanished long ago.

Murals on the walls depict their history - a rise to greatness, 
hubris that angered the gods, and a catastrophic fall. The swamp, 
it seems, was their punishment.

In what was once a throne room, you find their last king - still 
sitting on his throne, a skeleton draped in rotting finery.""",
            routes=[
                Route(1, "sunken_ruins", "Return to the ruins entrance", danger_level=2),
                Route(2, "throne_room", "Approach the skeleton king", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("skeleton")],
            items=[ItemFactory.create_item("gold coins"), ItemFactory.create_item("gemstone")],
            features=["collapsed hallways", "historical murals", "throne room", "skeleton king"],
            dangerous=True,
            danger_level=3,
            ambient_sounds=["stone crumbling", "water dripping", "ancient whispers"]
        )
        
        locations["throne_room"] = Location(
            location_id="throne_room",
            name="Sunken Throne Room",
            description="The throne room of a forgotten king.",
            long_description="""The skeleton on the throne wears a crown of tarnished gold and 
holds a scepter in its bony grip. Even in death, there's something 
regal about its posture.

As you approach, the skeleton's head turns to face you. Empty eye 
sockets seem to see into your soul.

"Another visitor," it says, its voice like wind through dry leaves. 
"Come to rob the dead, or to hear their wisdom?"

The skeleton king is not entirely dead, it seems.""",
            routes=[
                Route(1, "ruins_upper", "Back away from the throne", danger_level=1),
            ],
            creatures=[CreatureFactory.create_creature("ghost")],
            items=[ItemFactory.create_item("royal crown"), ItemFactory.create_item("ancient artifact")],
            features=["skeleton king", "tarnished crown", "undead awareness", "ancient wisdom"],
            special_actions=["speak with king", "attack", "bow", "ask for treasure"],
            ambient_sounds=["hollow voice", "bones creaking", "ancient memories"]
        )
        
        locations["ruins_submerged"] = Location(
            location_id="ruins_submerged",
            name="Submerged Ruins",
            description="Diving into the flooded lower levels.",
            long_description="""The water is murky but you can see enough to navigate. The lower 
levels are surprisingly intact, preserved by the water that 
destroyed them.

Treasures litter the floors - gold, gems, artifacts of a forgotten 
age. But you're not alone down here. Pale shapes drift through 
the water - the drowned dead, still guarding their domain.

You'll need to be quick. Your air won't last forever.""",
            routes=[
                Route(1, "sunken_ruins", "Surface quickly", danger_level=3),
            ],
            creatures=[CreatureFactory.create_creature("ghost"), CreatureFactory.create_creature("ghost")],
            items=[ItemFactory.create_item("gold coins"), ItemFactory.create_item("gold coins"),
                   ItemFactory.create_item("gemstone"), ItemFactory.create_item("ancient artifact"),
                   ItemFactory.create_item("golden key")],
            features=["flooded chambers", "preserved treasures", "drowned dead", "limited air"],
            water=True,
            dark=True,
            dangerous=True,
            danger_level=5,
            ambient_sounds=["bubbling", "muffled sounds", "ghostly moaning"]
        )
        
        # ===================================================================
        # MOUNTAIN PATH AND TOWER
        # ===================================================================
        locations["mountain_path"] = Location(
            location_id="mountain_path",
            name="Mountain Path",
            description="A winding path leading up into the mountains.",
            long_description="""The forest gives way to rocky terrain as the path climbs toward 
the mountains. The air grows cooler and thinner, and you can see 
snow on the peaks above.

The path is treacherous - narrow ledges, loose rocks, and sheer 
drops. One wrong step could be fatal.

Ahead, you can see the stone tower you spotted from afar, perched 
on a mountain ledge. It looks ancient and abandoned, but you 
notice a light flickering in one of its windows.""",
            routes=[
                Route(1, "cliff_top", "Return to the cliff top", danger_level=2),
                Route(2, "maze_exit", "Return through the forest", danger_level=2),
                Route(3, "tower_base", "Continue to the tower", danger_level=3),
                Route(4, "mountain_cave", "Explore a cave entrance to the side", danger_level=3),
            ],
            items=[ItemFactory.create_item("stone"), ItemFactory.create_item("healing herb")],
            features=["rocky terrain", "narrow ledges", "distant tower", "flickering light"],
            climbable=True,
            dangerous=True,
            danger_level=3,
            ambient_sounds=["wind howling", "rocks falling", "eagles crying"]
        )
        
        locations["mountain_cave"] = Location(
            location_id="mountain_cave",
            name="Mountain Cave",
            description="A cave carved into the mountainside.",
            long_description="""The cave appears to be both natural and worked - the entrance is 
natural stone, but deeper in you can see carved walls and steps.

The air is warmer here than outside, heated by something deep within 
the mountain. A faint red glow emanates from below, and you can 
smell sulfur.

This cave leads to something volcanic... and ancient.""",
            routes=[
                Route(1, "mountain_path", "Return to the mountain path", danger_level=1),
                Route(2, "volcanic_chamber", "Descend toward the red glow", danger_level=5),
            ],
            items=[ItemFactory.create_item("iron ore"), ItemFactory.create_item("ember crystal")],
            features=["worked stone", "warm air", "red glow", "sulfur smell"],
            dark=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["rumbling", "hissing steam", "distant roaring"]
        )
        
        locations["volcanic_chamber"] = Location(
            location_id="volcanic_chamber",
            name="Volcanic Chamber",
            description="A massive chamber filled with lava and heat.",
            long_description="""The cave opens into an enormous chamber filled with rivers of 
molten rock. The heat is nearly unbearable, and the air shimmers.

But you're not alone. Coiled around a pillar of obsidian, scales 
gleaming like molten gold, rests a creature of legend - a dragon.

It's not as massive as the tales describe, but it's still 
terrifying. Its eyes open, fixing upon you with ancient intelligence.

"A visitor," it rumbles. "How... unexpected."

This could be the end of your journey... or its greatest triumph.""",
            routes=[
                Route(1, "mountain_cave", "Try to flee before it attacks", danger_level=4),
            ],
            creatures=[CreatureFactory.create_creature("ancient dragon")],
            items=[ItemFactory.create_item("dragon scale"), ItemFactory.create_item("flame sword"),
                   ItemFactory.create_item("gold coins"), ItemFactory.create_item("gold coins"),
                   ItemFactory.create_item("royal crown")],
            features=["lava rivers", "obsidian pillar", "dragon", "unbearable heat"],
            dangerous=True,
            danger_level=5,
            special_actions=["speak with dragon", "attack", "offer tribute", "flee"],
            ambient_sounds=["lava bubbling", "dragon breathing", "stone cracking"]
        )
        
        locations["tower_base"] = Location(
            location_id="tower_base",
            name="Tower Base",
            description="At the base of the ancient stone tower.",
            long_description="""The tower rises before you, built of dark stone that seems to 
absorb light. It's ancient - older than any structure you've seen, 
covered in symbols that hurt to look at directly.

The heavy wooden doors are locked with a mechanism that requires 
a special key - the Tower Key, according to a plaque beside the 
door. Without it, you cannot enter.

Through the arrow slits, you can see movement - something lives 
here still.""",
            routes=[
                Route(1, "mountain_path", "Return down the mountain", danger_level=2),
                Route(2, "tower_interior", "Enter the tower", 
                      danger_level=4, requires_item="tower key"),
                Route(3, "tower_exterior", "Circle around the tower exterior", danger_level=2),
            ],
            features=["dark stone", "ancient symbols", "locked doors", "movement inside"],
            dangerous=True,
            danger_level=3,
            ambient_sounds=["wind whistling", "something moving inside", "stone groaning"]
        )
        
        locations["tower_exterior"] = Location(
            location_id="tower_exterior",
            name="Tower Exterior",
            description="Walking around the outside of the tower.",
            long_description="""Circling the tower, you find it's built on the very edge of a 
cliff. The view is stunning - you can see the entire forest spread 
out below, the swamp to the east, the mountains continuing to the 
west.

On the far side of the tower, you find a small shrine with a key 
resting on it - the Tower Key, left here by some previous visitor 
who never made it inside.

There's also what looks like a hidden entrance, partially concealed 
by rubble.""",
            routes=[
                Route(1, "tower_base", "Return to the front of the tower", danger_level=0),
                Route(2, "tower_secret", "Investigate the hidden entrance", danger_level=3),
            ],
            items=[ItemFactory.create_item("tower key"), ItemFactory.create_item("map fragment")],
            features=["cliff edge", "stunning view", "small shrine", "hidden entrance"],
            climbable=True,
            ambient_sounds=["wind howling", "eagles crying", "distant sounds below"]
        )
        
        locations["tower_secret"] = Location(
            location_id="tower_secret",
            name="Tower Secret Entrance",
            description="A hidden way into the tower.",
            long_description="""The rubble conceals a small tunnel that leads into the tower's 
basement. It's tight and dark, requiring you to crawl, but it's 
passable.

The tunnel opens into a storage room filled with old crates and 
barrels. Whatever the tower was used for, they kept supplies 
for a long siege.

Stairs lead up into the main tower.""",
            routes=[
                Route(1, "tower_exterior", "Crawl back outside", danger_level=1),
                Route(2, "tower_basement", "Explore the storage room", danger_level=2),
                Route(3, "tower_interior", "Climb the stairs into the tower", danger_level=3),
            ],
            items=[ItemFactory.create_item("dried meat"), ItemFactory.create_item("rope"),
                   ItemFactory.create_item("torch")],
            features=["tight tunnel", "storage room", "old supplies", "stairs up"],
            dark=True,
            ambient_sounds=["rats scurrying", "your breathing", "creaking above"]
        )
        
        locations["tower_basement"] = Location(
            location_id="tower_basement",
            name="Tower Basement",
            description="The storage basement of the tower.",
            long_description="""The basement is filled with supplies that have been here for 
centuries - most rotted away, but some preserved by the cold, 
dry conditions.

Among the supplies, you find equipment that belonged to the tower's 
original inhabitants - robes, books, and strange instruments. This 
was a wizard's tower, you realize, used for arcane experiments.

One section of the basement is sealed with magical wards, still 
glowing faintly after all these years.""",
            routes=[
                Route(1, "tower_secret", "Return to the secret entrance", danger_level=0),
                Route(2, "tower_interior", "Climb the stairs up", danger_level=3),
                Route(3, "sealed_chamber", "Break the magical seals", 
                      danger_level=5, requires_skill=(SkillType.MAGIC, 5)),
            ],
            items=[ItemFactory.create_item("mana potion"), ItemFactory.create_item("old journal"),
                   ItemFactory.create_item("cloth")],
            features=["preserved supplies", "wizard's equipment", "sealed section", "magical wards"],
            dark=True,
            ambient_sounds=["magical humming", "settling dust", "your footsteps"]
        )
        
        locations["sealed_chamber"] = Location(
            location_id="sealed_chamber",
            name="Sealed Chamber",
            description="A chamber sealed by ancient magic.",
            long_description="""The wards shatter as you break them, releasing a burst of stale 
air that hasn't moved in centuries. Inside, you find the wizard's 
private laboratory - and his final experiment.

A creature of pure magic floats in a containment circle, dormant 
but not dead. It was created here, and when its creator died, it 
simply... waited.

Around it, you see the wizard's greatest treasures - artifacts of 
immense power that he never had the chance to use.""",
            routes=[
                Route(1, "tower_basement", "Leave the chamber", danger_level=2),
            ],
            items=[ItemFactory.create_item("enchanted staff"), ItemFactory.create_item("ring of regeneration"),
                   ItemFactory.create_item("amulet of protection"), ItemFactory.create_item("elixir of life")],
            features=["containment circle", "dormant creature", "wizard's treasures", "ancient magic"],
            dark=True,
            dangerous=True,
            danger_level=5,
            special_actions=["release creature", "destroy creature", "bind creature"],
            ambient_sounds=["magical resonance", "creature breathing", "power humming"]
        )
        
        locations["tower_interior"] = Location(
            location_id="tower_interior",
            name="Tower Interior",
            description="Inside the ancient wizard's tower.",
            long_description="""The tower's interior is a vertical maze of staircases, platforms, 
and chambers. Magical artifacts hang suspended in the air, books 
float from shelf to shelf, and ghostly lights illuminate the space.

The wizard who built this place was incredibly powerful - even 
centuries after his death, his magic maintains itself.

At the very top of the tower, you can see a massive window looking 
out over the forest. That's where you need to go.

But something guards the way - the wizard's last, greatest creation.""",
            routes=[
                Route(1, "tower_base", "Exit through the front door", danger_level=0),
                Route(2, "tower_secret", "Exit through the secret passage", danger_level=0),
                Route(3, "tower_top", "Climb to the tower top", danger_level=4),
            ],
            creatures=[CreatureFactory.create_creature("wraith")],
            items=[ItemFactory.create_item("mana potion"), ItemFactory.create_item("glowing crystal")],
            features=["vertical maze", "floating artifacts", "ghostly lights", "guardian creature"],
            dark=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["magical humming", "pages turning", "guardian moving"]
        )
        
        locations["tower_top"] = Location(
            location_id="tower_top",
            name="Tower Top",
            description="The summit of the wizard's tower.",
            long_description="""You've reached the top. The view is extraordinary - from here, 
you can see everything. The entire forest spread out like a map, 
the swamp, the mountains, the paths you've traveled.

And there, in the distance, you see it - the edge of the forest. 
The way out. It's real. Escape is possible.

But first, you must deal with what waits here. The wizard may be 
dead, but his final guardian remains - a construct of pure magic, 
bound to protect this place forever.

Beyond it, you can see the wizard's final gift - a portal that 
leads out of the forest entirely.""",
            routes=[
                Route(1, "tower_interior", "Retreat back down the tower", danger_level=2),
                Route(2, "final_battle", "Face the guardian", danger_level=5),
            ],
            creatures=[CreatureFactory.create_creature("shadow beast")],
            items=[ItemFactory.create_item("mysterious map")],
            features=["extraordinary view", "forest edge visible", "portal", "final guardian"],
            dangerous=True,
            danger_level=5,
            ambient_sounds=["wind howling", "magic crackling", "guardian's challenge"]
        )
        
        locations["final_battle"] = Location(
            location_id="final_battle",
            name="Final Confrontation",
            description="The last battle before freedom.",
            long_description="""The guardian stands between you and the portal - a creature of 
shadow and light, bound by the wizard's will to protect this place 
for eternity.

It doesn't speak, but you feel its challenge in your mind. It has 
tested countless others, and all have failed. Their bones litter 
the floor around the portal.

But you've come too far to fail now. You've survived the forest, 
its creatures, its magic, and its darkness. This is your final 
test.

Defeat the guardian, and the portal is yours. Freedom awaits.""",
            routes=[
                Route(1, "tower_top", "Retreat to plan", danger_level=3),
                Route(2, "freedom", "Step through the portal after victory", danger_level=0),
            ],
            creatures=[CreatureFactory.create_creature("shadow beast")],
            items=[ItemFactory.create_item("guardian blade"), ItemFactory.create_item("sunstone")],
            features=["shadow guardian", "portal to freedom", "bones of failures", "final test"],
            dangerous=True,
            danger_level=5,
            ambient_sounds=["reality warping", "guardian's power", "portal humming", "your heartbeat"]
        )
        
        locations["freedom"] = Location(
            location_id="freedom",
            name="Freedom",
            description="You have escaped the Whispering Woods.",
            long_description="""The portal deposits you on a hillside overlooking a valley. 
Behind you, the forest is visible as a dark mass on the horizon, 
but it no longer has power over you.

You're free.

The sun is setting, painting the sky in brilliant oranges and 
purples. In the valley below, you can see a village - smoke rising 
from chimneys, people going about their lives.

You've done it. Against all odds, you've escaped the Whispering 
Woods. The nightmare is over.

But you know, deep down, that the forest is still there. Still 
waiting. Still claiming victims.

Perhaps one day, you'll return. But for now... you're free.""",
            routes=[],
            features=["freedom", "village below", "sunset", "end of nightmare", "new beginning"],
            rest_allowed=True,
            save_point=True,
            ambient_sounds=["birds singing", "wind in grass", "distant village sounds", "peace"]
        )
        
        # ===================================================================
        # SACRED GROVE (from cave exit)
        # ===================================================================
        locations["sacred_grove"] = Location(
            location_id="sacred_grove",
            name="Sacred Grove",
            description="A grove sacred to the spirits of the forest.",
            long_description="""You emerge from the cave into a place of profound beauty and peace. 
Ancient trees form a perfect circle around a clearing carpeted with 
soft grass and wildflowers. A spring bubbles up at the center, its 
water crystal clear.

The air here feels different - charged with life and magic. You 
can sense the presence of spirits, benevolent ones, watching over 
this place.

This is a sanctuary. Whatever darkness lurks in the forest cannot 
reach here.""",
            routes=[
                Route(1, "cave_exit", "Return through the cave", danger_level=1),
                Route(2, "spirit_spring", "Approach the spring", danger_level=0),
                Route(3, "fairy_grove", "Follow the path through the flowers", danger_level=0),
            ],
            items=[ItemFactory.create_item("healing herb"), ItemFactory.create_item("healing herb"),
                   ItemFactory.create_item("healing herb")],
            creatures=[CreatureFactory.create_creature("tree spirit")],
            features=["ancient trees", "wildflower carpet", "crystal spring", "benevolent presence"],
            rest_allowed=True,
            save_point=True,
            ambient_sounds=["spring bubbling", "birds singing", "wind chimes", "peaceful humming"]
        )
        
        locations["spirit_spring"] = Location(
            location_id="spirit_spring",
            name="Spirit Spring",
            description="A magical spring at the heart of the sacred grove.",
            long_description="""The spring is unlike any water you've seen - it glows faintly 
from within, and you can see small motes of light dancing in its 
depths. The water is warm and smells of flowers.

Drinking from this spring is said to restore body and soul. It 
might even grant visions of the future... or the past.

At the edge of the spring sits a spirit - humanoid but made of 
living light. It regards you with curiosity.""",
            routes=[
                Route(1, "sacred_grove", "Return to the grove", danger_level=0),
            ],
            creatures=[CreatureFactory.create_creature("tree spirit")],
            items=[ItemFactory.create_item("spirit essence"), ItemFactory.create_item("elixir of life")],
            features=["glowing water", "dancing lights", "warm spring", "light spirit"],
            water=True,
            special_actions=["drink from spring", "speak with spirit", "meditate"],
            ambient_sounds=["water tinkling", "spirit humming", "otherworldly music"]
        )
        
        # ===================================================================
        # DEAD FOREST AND ROPE BRIDGE
        # ===================================================================
        locations["rope_bridge"] = Location(
            location_id="rope_bridge",
            name="Rope Bridge",
            description="A rickety rope bridge spanning a deep gorge.",
            long_description="""The bridge sways alarmingly as you step onto it. Rotten planks and 
frayed ropes are all that separate you from a fall of hundreds of 
feet into the rocky gorge below.

Each step is a test of courage. The wind picks up, making the 
bridge swing wildly. Some planks are missing entirely, requiring 
you to jump over gaps.

On the other side, the stone tower awaits.""",
            routes=[
                Route(1, "cliff_top", "Return to the cliff", danger_level=2),
                Route(2, "tower_base", "Cross to the tower", danger_level=3),
            ],
            features=["swaying bridge", "missing planks", "deep gorge", "frayed ropes"],
            dangerous=True,
            danger_level=3,
            ambient_sounds=["wind howling", "ropes creaking", "planks groaning", "your heartbeat"]
        )
        
        locations["dead_forest_edge"] = Location(
            location_id="dead_forest_edge",
            name="Edge of the Dead Forest",
            description="Where the living forest meets the dead.",
            long_description="""Here, the transition is stark and sudden. On one side, healthy 
trees with green leaves. On the other, blackened trunks with 
bare branches, ground covered in ash and dead leaves.

No birds sing in the dead forest. No insects buzz. Even the wind 
seems reluctant to enter.

Whatever killed this part of the forest left it poisoned. You can 
feel the wrongness radiating from the dead trees.""",
            routes=[
                Route(1, "cliff_top", "Return to the cliff top", danger_level=1),
                Route(2, "dead_forest", "Enter the dead forest", danger_level=4),
            ],
            features=["stark transition", "blackened trees", "ash ground", "wrongness"],
            dangerous=True,
            danger_level=3,
            ambient_sounds=["silence", "occasional creak", "your footsteps in ash"]
        )
        
        locations["dead_forest"] = Location(
            location_id="dead_forest",
            name="Dead Forest",
            description="A forest killed by dark magic.",
            long_description="""Every tree here is dead - not just bare, but blackened and 
twisted as if by fire, though no fire could have done this. The 
ground is covered in ash that muffles your footsteps.

The silence is absolute and oppressive. You feel watched by 
something malevolent, though you see nothing.

At the center of the dead forest, you can see a structure - some 
kind of altar or monument to whatever power destroyed this place.""",
            routes=[
                Route(1, "dead_forest_edge", "Return to the living forest", danger_level=3),
                Route(2, "corruption_source", "Investigate the central structure", danger_level=5),
            ],
            creatures=[CreatureFactory.create_creature("wraith"), CreatureFactory.create_creature("skeleton")],
            items=[ItemFactory.create_item("shadow essence")],
            features=["dead trees", "ash ground", "absolute silence", "central structure"],
            dark=True,
            dangerous=True,
            danger_level=4,
            ambient_sounds=["oppressive silence", "occasional crack", "your breathing"]
        )
        
        locations["corruption_source"] = Location(
            location_id="corruption_source",
            name="Source of Corruption",
            description="The origin point of the forest's death.",
            long_description="""The structure is an altar, built of obsidian and bone. On it rests 
a crystal of pure darkness - the source of the corruption that 
killed this forest and spreads still to claim more.

The crystal pulses with malevolent energy. You can feel it trying 
to enter your mind, to corrupt you as it corrupted the trees.

Destroying the crystal could save the forest - or it could release 
whatever is trapped inside.""",
            routes=[
                Route(1, "dead_forest", "Retreat from the altar", danger_level=3),
            ],
            items=[ItemFactory.create_item("shadow essence"), ItemFactory.create_item("shadow essence"),
                   ItemFactory.create_item("shadow cloak")],
            features=["obsidian altar", "dark crystal", "corruption source", "trapped evil"],
            dark=True,
            dangerous=True,
            danger_level=5,
            special_actions=["destroy crystal", "absorb power", "seal crystal", "flee"],
            ambient_sounds=["dark pulsing", "whispered corruption", "reality straining"]
        )
        
        return locations


