====================
Before You Deprecate
====================

Regret is painful.

Making a design or implementation mistake and having to pay for it later can be a significant burden [#]_ for a library, package or codebase.
This burden weighs heavily both on maintainer(s) and on users of the code.

Most of the functionality provided by :ref:`regret` is aimed towards these inevitable moments *after* a mistake has been made and is to be corrected.

However, there are a number of things that can be done *before* any mistake has even been made, which may minimize the need for some deprecations, or minimize their damage, or increase the overall trust between you the maintainer and your package's users.

This document discusses a number of these concerns -- things you should do as a maintainer before you even do any deprecations at all.

.. [#]  a burden this library tries to ease, at least a small bit


Have a Policy
-------------

The most important thing a maintainer can do ahead of time is to have a clear and understandable deprecation *policy*.

The policy can be as formal or informal as appropriate, or as may be known ahead of time.

It should clearly communicate what users of a package can expect out of you the maintainer when a deprecation is needed. It may cover any or all of:

    * once a deprecation has been done, how long will it be before the deprecation is finished and the object is removed or changed incompatibly?

    * where or how will deprecations be communicated?

    * how do you the maintainer, or team of maintainers, view backwards compatibility in the context of your package?
      Is it important?
      Is it unimportant (sometimes it won't be!)

    * in the event a backwards incompatible change is made *unintentionally*, perhaps due to the introduction of a bug, is fixing the backwards incompatibility itself allowed as a backwards incompatibility in a successive release? Does the answer change if the bug is unnoticed for a long while?

    * how will changes to the deprecation policy itself be done?

Your policy will likely fail to predict all of the intricate deprecations that you may need over your package's long and healthy lifetime.
Judgment calls may still have to be made (`empathetically <before-you-deprecate:Empathize>`), but a policy sets an initial set of guidelines which can be built upon later.


.. seealso::

    :pep:`387`

        The PEP covering the backwards compatibility policy for Python itself
        as a language

    `compatibility`

        :ref:`regret`'s own deprecation policy

    `Twisted Compatibility Policy <https://docs.twisted.org/en/stable/development/compatibility-policy.html>`_

        The Twisted project's deprecation (compatibility) policy


Document Your Public API
------------------------

A `deprecation policy <before-you-deprecate:Have a Policy>` can clarify to users of a package what to expect as the package evolves and changes APIs or objects over time.

Simply specifying how deprecations will be handled however is not enough.
Even with a clear policy on how deprecations will be handled, a key additional piece of guidance is needed around *what objects or APIs are themselves considered "public" and thereby fall under the deprecation policy* [#]_.

As an uncontroversial non-example to illustrate -- the specific layout of lines of code within a package's source code is essentially never part of a package's public API.
Adding a blank line, or a comment, or even reordering the order in which two functions are defined in a file is essentially universally treated as an acceptable change to make without any indication.
This is the case even though in theory [#]_ a downstream user of the package may have written code that relies on exact line numbers of an object, or on the ordering of definitions of objects
within the package.

Within the (Python) community, there is a generally agreed upon set of fundamental norms that most maintainers follow or understand, which covers a portion of this public API definition.
But there are a number of areas or subtleties where there is no explicitly discussed standard practice -- and in these cases there are maintainers and libraries which conduct themselves in different ways (i.e. which do or do not consider these parts of their API surface to be public or private).

And so -- having clear guidelines on what part of a package's APIs are considered public can be hugely helpful for users who wish to understand when and where they are using a package as intended, and can therefore rely on its policy.

Here is a (non-exhaustive) list of potential API surface that you may need or want to clarify:

    * for "normal" Python function parameters which may be passed either positionally or by name, is the order of parameters considered public and will not change?
      How about their names?
      Will they change?
      How about the kind of parameter itself?
      Will positional parameters always be passable positionally?
      Or may a parameter "convert" into a keyword-only one, or vice versa?

    * does the package use a convention to indicate entire modules within it are considered private?
      (say, :samp:`{mypackage}._{foo}`, following that of other Python objects)

    * is the text content of exceptions defined or raised by the package part of its public API, or may they change?

    * which methods on objects are considered part of their public API?
      Is their ``__repr__`` considered private, even though it otherwise follows public API conventions?
      Are any other methods considered similarly exceptional to the "rule"?

    * are modules and objects found within the package's test suite considered public API?

    * are imported objects part of a module's public API?
      Can a user of the package assume that if ``mypackage.foo`` imports ``bar``, even though ``bar`` really lives in some other module, that ``bar`` will not be removed from ``mypackage.foo``?
      Is the answer different if ``bar`` is an object defined somewhere in ``mypackage`` vs. in an external package?

    * is the layout of your documentation considered public API?
      More specifically for say, a package documenting itself via `Sphinx <sphinx:index>`, will the `refs <ref>` defined for headings be kept over time?
      Will the overall document structure change?
      How about links to specific concrete pages as URLs?

    * is being able to *raise* exceptions defined by your library part of its public API?
      Or is only catching them considered public?

    * is the number of stack frames your library uses internally to implement a public API itself public API?
      After all, a downstream library calling into it may be using `warnings.warn` and be providing a ``stacklevel`` parameter relying on it!

    * a class in your library is defined using `attrs <attrs:index>`.
      Is calling `attrs.evolve` directly on instances of your class considered public API, and your class is thereby permanently coupled to `attrs.evolve`'s public API?
      Or is your use of ``attrs`` as a library maintainer simply an implementation detail?

    * a function in your library calls `requests.get`, a function which has mutable global state -- it allows someone to import the library and e.g. define `Transport Adapters <requests:transport-adapters>` which, even if done outside your library, affect how it will retrieve the HTTP response.
      Is your library free to change its HTTP client to another HTTP client even though this will potentially disrupt users who expect their external change to have an effect on your library's behavior?

    * your package depends on ``foo>1.2.3``. Are these pins part of your public API, and bumping the lower-pinned version of ``foo`` a breaking change? Doing so may of course affect users who are using ``foo==1.2.3`` alongside another of their own dependencies.

    * today, your package has no binary (non-Python) dependencies. Is that a permanent promise of its installation "API"?

    * ...

There are many many more.
Think of things that you, a maintainer, rely on from libraries *you* use, and how many subtleties you wish were clearer.

To be clear, some of the above *do* have commonly understood answers in the ecosystem -- but even beyond resolving the final bits of doubt, there may still be a lot to gain from explicitly confirming each has been considered in the course of changes made to the package.


.. [#] Python does not have a particularly formal enforced definition of "public" and "private", but we use the terms here in their commonly understood meaning within the Python ecosystem: a public object or API is one which is expected to be relied upon by end-users of the package and whose compatibility is "guaranteed", and a private object is one whose use is conversely *not* encouraged and not guaranteed for end users, regardless of its accessibility at runtime.

.. [#] though hopefully not in practice, even if `Hyrum's Law <https://www.hyrumslaw.com/>`_ might apply.


.. seealso::

    `public API <compatibility:Public API>`

        :ref:`regret`'s own public API definition

    `The SemVer specification, step 1 <https://semver.org/#semantic-versioning-specification-semver>`_

        which echoes the requirement of defining a clear public API.

    `jsonschema public API <jsonschema:faq:how do jsonschema version numbers work?>`

        another example of a public API definition


Empathize
---------

Having a `policy <before-you-deprecate:Have a Policy>` for how you'll deprecate things, and having a `definition <before-you-deprecate:Document Your Public API>` of what it is that is subject to deprecation are key steps in setting clear expectations.

The reality is -- they'll never be enough.

End-users of your package will forget or not notice something isn't part of your public API. Or they'll knowingly rely on things that aren't public given "no other" good option for a particular piece of functionality.

Be empathetic!
We are all just trying to get our jobs done, whatever they may be.

Empathy in this case means -- if you've clearly defined something as private, but you nonetheless see thousands of uses of the private API in downstream code, simply take pause.
At the very least, this often may indicate either a UX issue in finding the appropriate public APIs (which can be used to improve your package's overall experience) or the lack of an API entirely.

An API marked "experimental" and not-to-be-relied-upon will *still* be relied upon if it remains unchanged for a number of years in the wild, and breaking it, while justified, will still break downstream users.
Do so knowingly, if you do do so.

You may choose not to remove a *private* API if it would cause significant breakage due to its evident use.
Doing so indicates empathy!
(Though, in contrast, *not* doing so, and removing the API, should not be weaponized into a *lack* of empathy!)


Take situations like these as ways to improve the clarity of your policies and guidance of your documentation overall, and as ways to build healthy relationships, *if* that is your decision.


Analytics
---------

As a final area of consideration, though a challenging one -- nothing beats data.

If you as a package author have access to concrete usage data of any kind, use it to make better decisions about your package's evolution.

In simple cases this may be as simple as answering "can I deprecate support for a particular Python version?" by investigating how many installations of your package are done on the version in question, for which `the PyPA provides a dataset that can help <packaging:guides/analyzing-pypi-package-downloads>`.
But the same questions can be asked of any API -- "how often is this function used? What data would help quantify its use, and can I access it?".

Any additional data you may have or can easily (and ethically) collect will help drive intelligent and informed decisions.
