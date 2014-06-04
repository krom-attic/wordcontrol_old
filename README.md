WordControl
===========

Word Control is an application for a collaboration on documenting endangered languages, especially its lexicon and phonology.

Development process (v. 2)
--------------------------
Any work to be done must be planned against some milestone. This planning is made by @kromkrom.

Work items are tasks:
* Enhancements
* Bugs
* Other tasks

Work items are created based on:
* Use cases (UC)
* Functions (F)
* Change requests (CRs)

Any new CR's effect is evaluated, then:
* If it affects business logic, it causes a new enhancement and is attached to a new or to an existing UC
* If it affects solution, it causes a new enhancement and is attached to a new or to an existing F
* If it affects code, but none of the above, it is a bug

A CR should be converted to a work item directly if there is no one-to-many (or more complex) relation between the CR and the work items.

After work planned for an UC or F is done, the results are recorded in the corresponding UC or F.
Any pending changes caused by CRs to UCs and Fs are made only after the current realisation state is documented.

Deployment process
------------------
This project is using South.
Create migration profile:
manage.py schemamigration wordengine --auto
Apply migration profile:
manage.py migrate wordengine

This project will use Fabric as soon as it is update for Python 3 (http://www.fabfile.org/).