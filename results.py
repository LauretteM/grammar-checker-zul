from enum import Enum

class GrammarResult(Enum):

    CORRECT = "This sentence looks good."
    NO_ERRORS_FOUND = "Could not identify agreement errors."

    QUAL_ADJ_AGREEMENT = "Check the agreement between the noun/pronoun and its qualifying adjective."
    QUAL_ID_NP_AGREEMENT = "Check the agreement between the noun/pronoun and its qualifying noun."
    QUAL_ASSOC_NP_AGREEMENT = "Check the agreement between the noun/pronoun and its qualifying associative noun."
    QUAL_LOC_AGREEMENT = "Check the agreement between the noun/pronoun and its qualifying locative expression."
    QUAL_VERB_AGREEMENT = "Check the agreement between the noun/pronoun and its qualifying verb phrase."
    
    SUBJ_ADJ_AGREEMENT = "Check the agreement between the noun/pronoun and the predicative adjective."
    SUBJ_ID_NP_AGREEMENT = "Check the agreement between the noun/pronoun and the predicate noun."
    SUBJ_ASSOC_NP_AGREEMENT = "Check the agreement between the noun/pronoun and the associative noun."
    SUBJ_LOC_AGREEMENT = "Check the agreement between the noun/pronoun and the locative predicate."
    SUBJ_VERB_AGREEMENT = "Check the agreement between the subject and verb."