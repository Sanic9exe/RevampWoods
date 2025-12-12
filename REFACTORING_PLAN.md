# Game Content Refactoring Plan

## Current State Analysis

### Content Counts (Current vs Target)
| Content Type | Current | Target | Reduction Needed |
|--------------|---------|--------|------------------|
| NPCs         | ~300    | 17     | Remove 283 (94%) |
| Items        | ~200+   | 60     | Remove 140+ (70%)|
| Creatures    | ~100+   | 50     | Remove 50+ (50%) |
| Locations    | ~70     | 50     | Remove 20 (29%)  |
| Achievements | ~150    | 20     | Remove 130 (87%) |
| Quests       | Current | 25     | Adjust to 25     |
| Crafting     | Current | 20     | Adjust to 20     |
| Companions   | Current | 15     | Adjust to 15     |
| Lore Entries | Current | 15     | Adjust to 15     |
| Random Events| ~200    | TBD    | Reduce           |

### File Sizes
- `data_store.py`: 67,803 lines (needs major reduction)
- `admin.py`: 119KB (needs simplification)

## Required Changes

### 1. Content Reduction (Priority: High, Effort: Very Large)

#### NPCs (300 → 17)
- Review all 300 NPCs
- Select 17 most unique/essential characters
- Ensure they cover different professions and locations
- Maintain meaningful backstories and dialogue
- Remove 283 NPCs

#### Items (200+ → 60)
- Categorize current items
- Select best weapons, armor, consumables, tools
- Ensure no redundancy
- Balance stats
- Focus on purposeful items only

#### Creatures (100+ → 50)
- Keep variety: Normal, Elite, Boss, Legendary
- Ensure appropriate difficulty progression
- Include mini-bosses and bosses
- Balance loot drops

#### Locations (70 → 50)
- Keep most detailed and unique areas
- Ensure proper connections
- Remove redundant or similar locations

#### Achievements (150 → 20)
- Select most meaningful achievements
- Cover different aspects: combat, exploration, quests, etc.
- Remove bloat achievements

#### Weather System
- Significantly reduce weather pattern content
- Keep core functionality
- Remove excessive variations

### 2. Admin Panel Cleanup (Priority: Medium, Effort: Medium)

#### Remove Browsing Features
- Command 40: Browse Expanded Creatures
- Command 41: Browse Expanded Items
- Command 42: Browse NPCs
- Command 44: Browse Combat Maneuvers
- Command 45: Read Lore (keep lore in game, not admin)
- Command 46: Browse Weather Patterns
- Command 47: Browse Status Effects
- Command 48: Browse Expanded Locations

#### Merge Duplicate Menus
- **Teleport**: Merge command 8 and 54 into single teleport
- **Spawn Creature**: Merge commands 10, 37, 49 into single spawn menu
- **Give Item**: Merge command 5 and 50 into single item menu

#### Consolidate Expanded Features
- Remove distinction between "normal" and "expanded" content
- Single unified system for all content

### 3. System Validation (Priority: High, Effort: Medium)

Ensure these systems work properly:
- ✓ Save/Load (already implemented)
- ✓ Quest System (check for 25 quests)
- ✓ Crafting (check for 20 recipes)
- ? Companion Management (verify works)
- ? Achievement Tracking (verify with 20 achievements)
- ? Magic/Spells System (verify implementation)
- ? Reputation System (verify implementation)
- ? Random Events (verify and adjust count)
- ? Minigames (verify and ensure they're accessible)

### 4. Minigames Enhancement (Priority: Medium, Effort: Low)

Current minigames in data_store.py:
- Lockpicking Game
- Fishing Game
- Dice Game

Ensure they are:
- Accessible during gameplay
- Not just in data_store but integrated
- Working properly

## Implementation Strategy

### Option A: Quick Wins First (Recommended)
1. Fix admin panel (remove browsing, merge duplicates) - 2-3 hours
2. Verify all systems work - 1-2 hours
3. Then tackle content reduction in phases:
   - Phase 1: Achievements (150→20) - 2 hours
   - Phase 2: Locations (70→50) - 3 hours
   - Phase 3: Items (200→60) - 4 hours
   - Phase 4: Creatures (100→50) - 3 hours
   - Phase 5: NPCs (300→17) - 5 hours
   - Phase 6: Weather reduction - 2 hours

Total: ~22-24 hours

### Option B: Comprehensive at Once
Do everything in one go - requires 24+ hours of continuous work

### Option C: Critical Path Only
Focus on most impactful changes:
1. Admin panel cleanup
2. Top 3 content reductions (NPCs, Items, Achievements)
3. System validation

Total: ~12-14 hours

## Recommendation

Start with **Option A** - Quick wins first:
1. Admin panel is easiest to fix
2. Proves systems work
3. Then methodically reduce content
4. User can test incrementally

## Questions for User

1. Which priority: A (incremental), B (comprehensive), or C (critical path)?
2. For content reduction, any specific items/NPCs/creatures you want to keep?
3. Should I preserve any specific expanded content?
4. Timeline expectations?
