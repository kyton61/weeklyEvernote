from evernote.api.client import EvernoteClient

dev_token = "my developer token"

# Set up the NoteStore client
client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
noteStore = client.get_note_store()

# Make API calls
user = userStore.getUser()
print user.username

notebooks = noteStore.listNotebooks()
for notebook in notebooks:
	print "Notebook: ", notebook.name
