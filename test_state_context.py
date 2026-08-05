from state_machine import StateMachine
from context_chain import ContextChain
from context_types import MailBody, MailMeta, MailContext
from datetime import datetime, UTC

state = StateMachine()
chain = ContextChain()

# Initialize an email
mail = MailContext(
    meta = MailMeta(
        sender = 'x@example.com',
        receiver = 'y@example.com',
        subject = 'Meeting invite',
        timestamp = datetime.now(UTC)
    ),
    body = MailBody(
        plain_text = 'Prepare stuff for the meeting at 3pm tomorrow.'
    )
)

while not state.is_terminal():
    current_state = state.state.name
    chain.add_context(current_state, mail)
    print(f'[State changed]the current state: {current_state}')
    state.next()
    print(f'state={state.state.name}')

print('\nThe context chain')
for step in chain.get_all_steps():
    print(f'Step:{step} --> Content summary: {chain.get_context(step).body.plain_text}')