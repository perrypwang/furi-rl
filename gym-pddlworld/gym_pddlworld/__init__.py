from gym.envs.registration import register

register(
    id='lslite-v0',
    entry_point = 'gym_pddlworld.envs:LsLiteEnv',
)