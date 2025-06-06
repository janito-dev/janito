"""Handles LLM driver config preparation and execution modes."""
from janito.llm.driver_config import LLMDriverConfig
from janito.provider_config import get_config_provider
from janito.cli.verbose_output import print_verbose_info


def _choose_provider(args):
    provider = getattr(args, 'provider', None)
    if provider is None:
        provider = get_config_provider()
        if provider and getattr(args, 'verbose', False):
            print_verbose_info("Default provider", provider, style="magenta", align_content=True)
        elif provider is None:
            print("Error: No provider selected and no provider found in config. Please set a provider using '-p PROVIDER', '--set provider=name', or configure a provider.")
            return None
    return provider

def _populate_driver_config_data(args, modifiers, provider, model):
    from janito.provider_config import get_effective_setting
    CONFIG_LOOKUP_KEYS = ("max_tokens", "base_url")
    driver_config_data = {"model": model}
    if getattr(args, 'verbose_api', None) is not None:
        driver_config_data['verbose_api'] = args.verbose_api
    for field in LLMDriverConfig.__dataclass_fields__:
        if field in CONFIG_LOOKUP_KEYS:
            if field in modifiers and modifiers[field] is not None:
                driver_config_data[field] = modifiers[field]
            else:
                value = get_effective_setting(provider, model, field)
                if value is not None:
                    driver_config_data[field] = value
        elif field in modifiers and field != "model":
            driver_config_data[field] = modifiers[field]
    return driver_config_data

def prepare_llm_driver_config(args, modifiers):
    provider = _choose_provider(args)
    if provider is None:
        return None, None, None
    from janito.provider_config import get_effective_model
    model = getattr(args, 'model', None)
    if not model:
        model = get_effective_model(provider)
    driver_config_data = _populate_driver_config_data(args, modifiers, provider, model)
    llm_driver_config = LLMDriverConfig(**driver_config_data)
    if getattr(llm_driver_config, 'verbose_api', None):
        pass
    agent_role = modifiers.get("role", "software developer")
    return provider, llm_driver_config, agent_role


def handle_runner(args, provider, llm_driver_config, agent_role, verbose_tools=False):

    zero_mode = getattr(args, 'zero', False)
    from janito.provider_registry import ProviderRegistry
    provider_instance = ProviderRegistry().get_instance(provider, llm_driver_config)
    mode = get_prompt_mode(args)
    if getattr(args, 'verbose', False):
        print_verbose_info("Active LLMDriverConfig (after provider)", llm_driver_config, style="green")
        print_verbose_info("Agent role", agent_role, style="green")
    if mode == "single_shot":
        from janito.cli.single_shot_mode.handler import PromptHandler as SingleShotPromptHandler
        handler = SingleShotPromptHandler(args, provider_instance, llm_driver_config, role=agent_role)
        handler.handle()
    else:
        from janito.cli.chat_mode.session import ChatSession
        from rich.console import Console
        console = Console()
        session = ChatSession(console, provider_instance, llm_driver_config, role=agent_role, args=args, verbose_tools=verbose_tools, verbose_agent=getattr(args, 'verbose_agent', False))
        session.run()

def get_prompt_mode(args):
    return 'single_shot' if getattr(args, 'user_prompt', None) else 'chat_mode'
