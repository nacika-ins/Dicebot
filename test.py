# coding: utf-8
from unittest import TestCase

import logic

def test_dice():
    result = logic.dice("@DiceBot 333")
    print(result)
    result = logic.dice("@DiceBot 10232")
    print(result)
    result = logic.dice("@DiceBot 5D5")
    print(result)
    result = logic.dice("@DiceBot        5D5")
    print(result)
    result = logic.dice(" @DiceBot -10")
    print(result)
    result = logic.dice('<p><span class="h-card"><a href="https://oransns.com/@QuizBot" class="u-url mention">@<span>QuizBot</span></a></span> 3333</p>')
    print(result)
    result = logic.dice('<p><span class="h-card"><a href="https://oransns.com/@QuizBot" class="u-url mention">@<span>QuizBot</span></a></span> 5D5</p>')
    print(result)
    result = logic.dice('<p><span class="h-card"><a href="https://oransns.com/@QuizBot" class="u-url mention">@<span>QuizBot</span></a></span> 5d5</p>')
    print(result)
