class ReplyMessage:
    WELCOME: str = (
        "Bienvenue dans le serveur Discord de l'ASETIN (Association des étudiantes et étudiants en informatique)! \n"
        "Afin de confirmer que tu es bel et bien un(e) étudiant(e) inscrit(e) à l'association, entre ton numéro d'identification personnel (NI).\n"
        "Au plaisir de te rencontrer!\n"
        "ps: Si tu ne sais pas où trouver ton NI, tu peux le consulter sur MonPortail ou encore sur ta carte étudiante."
    )

    ALREADY_REGISTERED: str = (
        "Your are already registered.\nIf you haven't registered yet, please contact an admin."
    )
    UNABLE_TO_REGISTER: str = (
        "Unable to registered you.\nCheck your NI. If your NI is the good one, please contact an admin."
    )

    SUCCESSFUL_REGISTRATION: str = (
        "You are now registered! Your role is now apply and your name is set."
    )

    SUCCESSFUL_STUDENT_ADDED: str = (
        "Student added ! He can now registered my himself by sending me a dm."
    )

    STUDENT_ALREADY_EXISTS: str = "This student already exists."

    MISSING_ARGUMENTS_IN_COMMAND: str = "Missing arguments in the command."
