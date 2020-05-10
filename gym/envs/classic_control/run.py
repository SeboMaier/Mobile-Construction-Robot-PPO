import gym
from stable_baselines.common.policies import MlpPolicy, MlpLnLstmPolicy
from stable_baselines.common.vec_env import VecNormalize, VecEnv, SubprocVecEnv, DummyVecEnv
from stable_baselines.common import set_global_seeds, make_vec_env, vec_env
from stable_baselines import PPO2
from stable_baselines.gail import generate_expert_traj, ExpertDataset

LOAD_TO_TRAIN = False


def make_env(env_id, rank, seed=0):
    """
    Utility function for multiprocessed env.
pip
    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = gym.make(env_id)

        env.seed(seed + rank)
        return env
    set_global_seeds(seed)
    return _init



def linear_schedule(initial_value):
    def func(progress):
        return progress * initial_value
    return func

if __name__ == '__main__':
    env_id = "Simulation-v0"
    num_cpu = 1
    # Create the vectorized environment
    venv = DummyVecEnv([lambda: gym.make("Simulation-v0")])
    nvenv = VecNormalize(venv, norm_obs=True, norm_reward=False)
    #env = SubprocVecEnv([make_env(env_id, i) for i in range(num_cpu)])
    # Stable Baselines provides you with make_vec_env() helper
    # which does exactly the previous steps for you:

    #venv = DummyVecEnv([lambda: gym.make("Simulation-v0")])
    #nvenv = VecNormalize(env, norm_obs=True, norm_reward=False)


    model = PPO2(MlpPolicy, nvenv, gamma=0.99, lam=0.95, nminibatches=4, noptepochs=4, learning_rate=linear_schedule(1e-4),
                 ent_coef=0.01, n_steps=2048, tensorboard_log="./logs/", verbose=1)

    generate_expert_traj(model, save_path="PPO2_100eps", n_episodes=100)

    #model.learn(total_timesteps=50000000, tb_log_name="PPO50M_constlr1e-5_hor2048_ent001_zeropad")
    #model.save("PPO50M_constlr1e-5_hor2048_ent001_zeropad")



    # tensorboard --logdir=logs --host localhost --port 8088
    # http://localhost:8088/
