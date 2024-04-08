import gymnasium as gym


def make_env(cfg, num_parallel_envs=0) -> gym.Env | gym.vector.SyncVectorEnv:
    """
    Note: When `num_parallel_envs > 0`, this function returns a `SyncVectorEnv` which takes batched action as input and
    returns batched observation, reward, terminated, truncated of `num_parallel_envs` items.
    """
    kwargs = {
        "obs_type": "pixels_agent_pos",
        "max_episode_steps": cfg.env.episode_length,
        "visualization_width": 384,
        "visualization_height": 384,
    }

    if cfg.env.name == "simxarm":
        import gym_xarm  # noqa: F401

        assert cfg.env.task == "lift"
        env_fn = lambda: gym.make(  # noqa: E731
            "gym_xarm/XarmLift-v0",
            **kwargs,
        )
    elif cfg.env.name == "pusht":
        import gym_pusht  # noqa: F401

        # assert kwargs["seed"] > 200, "Seed 0-200 are used for the demonstration dataset, so we don't want to seed the eval env with this range."
        env_fn = lambda: gym.make(  # noqa: E731
            "gym_pusht/PushTPixels-v0",
            **kwargs,
        )
    elif cfg.env.name == "aloha":
        import gym_aloha  # noqa: F401

        kwargs["task"] = cfg.env.task

        env_fn = lambda: gym.make(  # noqa: E731
            "gym_aloha/AlohaTransferCube-v0",
            **kwargs,
        )
    else:
        raise ValueError(cfg.env.name)

    if num_parallel_envs == 0:
        # non-batched version of the env that returns an observation of shape (c)
        env = env_fn()
    else:
        # batched version of the env that returns an observation of shape (b, c)
        env = gym.vector.SyncVectorEnv([env_fn for _ in range(num_parallel_envs)])
    return env
