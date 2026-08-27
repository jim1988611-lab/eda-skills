# PyAEDT source index

These are the primary sources used to build this skill. Prefer the versioned documentation that matches the installed AEDT/PyAEDT release. Links were reviewed on 2026-08-13.

## Official documentation

- Documentation home: https://aedt.docs.pyansys.com/
- Installation, bundled AEDT package, PyPI/Conda, uv, offline wheelhouse: https://aedt.docs.pyansys.com/version/stable/Getting_started/Installation.html
- Basic tutorial: https://aedt.docs.pyansys.com/version/stable/User_guide/intro.html
- Desktop sessions and lifecycle: https://aedt.docs.pyansys.com/version/dev/User_guide/desktop_sessions.html
- Versioning and gRPC/COM compatibility: https://aedt.docs.pyansys.com/version/stable/Getting_started/versioning.html
- PyAEDT 1.0 breaking changes: https://aedt.docs.pyansys.com/version/stable/release_1_0.html
- Release notes and compatibility updates: https://aedt.docs.pyansys.com/version/stable/changelog.html
- Client-server, secure gRPC, mTLS, WNUA, UDS: https://aedt.docs.pyansys.com/version/stable/Getting_started/ClientServer.html
- CLI: https://aedt.docs.pyansys.com/version/stable/Getting_started/cli.html
- Troubleshooting: https://aedt.docs.pyansys.com/version/stable/Getting_started/Troubleshooting.html
- User guide index: https://aedt.docs.pyansys.com/version/stable/User_guide/index.html
- Modeler: https://aedt.docs.pyansys.com/version/stable/User_guide/modeler.html
- Mesh: https://aedt.docs.pyansys.com/version/stable/User_guide/mesh.html
- Mesh user guide with Icepak global/local mesh examples: https://aedt.docs.pyansys.com/version/dev/User_guide/mesh.html
- Icepak mesh API and mesh classes: https://aedt.docs.pyansys.com/version/stable/API/Mesh.html
- Icepak local mesh-region API: https://aedt.docs.pyansys.com/version/stable/API/_autosummary/ansys.aedt.core.modules.mesh_icepak.IcepakMesh.assign_mesh_region.html
- Setup and sweeps: https://aedt.docs.pyansys.com/version/stable/User_guide/setup.html
- Variables and Optimetrics: https://aedt.docs.pyansys.com/version/stable/User_guide/variables.html
- Settings: https://aedt.docs.pyansys.com/version/stable/User_guide/settings.html
- Postprocessing: https://aedt.docs.pyansys.com/version/stable/User_guide/postprocessing.html
- Icepak API: https://aedt.docs.pyansys.com/version/stable/API/_autosummary/ansys.aedt.core.icepak.Icepak.html
- Icepak thermal boundary conditions: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v242/en/Subsystems/Icepak/Content/Icepak/AssigningThermalBoundaryConditionsinIcepak.htm
- Junction-to-case characterization: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ice_ug/ice_ug_sec_mdlpkg_junction_case.html
- Finned heat sink and turbulence setup: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v242/en/PDFs/Getting%20Started%20with%20Icepak%20-%20Finned%20Heat%20Sink.pdf
- Cold plate and natural/forced convection setup: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/PDFs/Getting%20Started%20with%20Icepak%20-%20Cold%20Plate%20Model.pdf
- Icepak setup templates: https://aedt.docs.pyansys.com/version/stable/API/SetupTemplatesIcepak.html
- Mesh API and Icepak mesh classes: https://aedt.docs.pyansys.com/version/stable/API/Mesh.html
- Icepak package objects and compact/detailed models: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ice_ug/ice_ug_chp_packages.html
- Delphi package characterization: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ice_ug/ice_ug_sec_delphi_pkg.html
- Delphi/STM optimization toolkit: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Icepak/Content/Variables/ToolkitIcepakExtractDelphiNetwork.htm
- 3DIC CTM import to Icepak: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Icepak/Content/Icepak/3DIntegratedCircuitsinIcepak.htm
- Delphi/STM training and testing workflow: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Icepak/Content/Variables/ToolkitIcepakExtractDelphiNetwork.htm
- Icepak Simplify command: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Icepak/Content/Modeler/SimplifyCommand.htm
- Icepak mesh-size region: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Icepak/Content/Mesh/CreatingaMeshSizeRegion.htm
- Non-conformal meshing for assemblies: https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ice_ug/ice_ug_sec_mesh_assy.html
- Icepak mesh quality getting-started example: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/PDFs/Getting%20Started%20with%20Icepak%20-%20Coil%20and%20Plate.pdf
- Extensions: https://aedt.docs.pyansys.com/version/stable/User_guide/extensions.html
- Extension command line launch: https://aedt.docs.pyansys.com/version/stable/User_guide/pyaedt_extensions_doc/commandline.html
- Security considerations: https://aedt.docs.pyansys.com/version/dev/User_guide/security_consideration.html
- Cheat sheet: https://aedt.docs.pyansys.com/version/stable/_static/cheat_sheet.pdf

## API and examples

- API reference: https://aedt.docs.pyansys.com/version/stable/API/
- Maxwell 3D API example: https://aedt.docs.pyansys.com/version/stable/API/_autosummary/ansys.aedt.core.maxwell.Maxwell3d.html
- End-to-end examples: https://examples.aedt.docs.pyansys.com/
- Examples repository: https://github.com/ansys/pyaedt-examples
- Main source repository and README: https://github.com/ansys/pyaedt
- PyEDB documentation: https://edb.docs.pyansys.com/
- OCP NIC thermal models: https://www.opencompute.org/wiki/Server/NIC
- OCP thermal simulation methodology: https://www.opencompute.org/wiki/Storage/Thermal_Sim_Methodology
- Icepak EM Loss from HFSS, Maxwell, or Q3D: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v252/en/Subsystems/Icepak/Content/Icepak/AssigningEMLossProperties.htm
- Icepak two-way coupling: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Icepak/Content/Icepak/AddingTwoWayCouplingtoanIcepakDesign.htm
- Icepak PCB and HFSS 3D Layout link: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v242/en/Subsystems/Icepak/Content/Icepak/PCBsinIcepak.htm
- Package Definition for Icepak thermal analysis: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/HFSS3DLayout/Content/3DLayout/CreatingOrEditingPackageDefinitionsForComponents.htm
- Icepak to Mechanical thermal transfer: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Mechanical/Content/Mechanical/SetupLink_ThermalCondition.htm
- Icepak coupling guides: https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v251/en/Subsystems/Icepak/Content/GettingStarted/IcepakGettingStartedGuides.htm
- RedHawk-SC Electrothermal and Icepak training: https://learninghub.ansys.com/learn/course/external/view/elearning/857/ansys-redhawk-sc-electrothermal-shi-yong-jing-que-deicepak-xi-tong-re-bian-jie-tiao-jian-jin-xing-gao-jing-du3dic-re-fang-zhen
- PyAEDT releases and wheelhouses: https://github.com/ansys/pyaedt/releases
- PyPI package: https://pypi.org/project/pyaedt/

## Scope and freshness

"All relevant data" cannot be permanently exhaustive because PyAEDT, AEDT service packs, API signatures, examples, and product integrations change. This skill therefore stores a curated official-source index and directs the agent to re-check versioned docs before using release-sensitive behavior. Community posts may be useful for hints, but should not override the official API, security, compatibility, or licensing guidance.
