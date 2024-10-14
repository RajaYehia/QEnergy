all: export plots

.PHONY: plots

plots: export/AlltoAll.pdf export/BB84detectstudy.pdf export/BB84QBERstudy.pdf export/BB84wavelengthstudy.pdf export/CKAstudydist.pdf export/CKAstudy.pdf export/CVVSDVstudy.pdf export/CVCKAstudy.pdf cv_plots export/EE.pdf export/MeasuredValues.pdf export/piecharts.pdf export/DVprotocolstudy.pdf export/timebinstudy.pdf

export:
	mkdir -p exports

export/AlltoAll.pdf:
	python3 studies/all_to_all.py

export/BB84detectstudy.pdf:
	python3 studies/bb84_detector.py

export/BB84QBERstudy.pdf:
	python3 studies/bb84_qber.py

export/BB84wavelengthstudy.pdf:
	python3 studies/bb84_wavelength.py

export/CKAstudydist.pdf:
	python3 studies/cka_dist.py

export/CKAstudy.pdf:
	python3 studies/cka.py

export/CVVSDVstudy.pdf:
	python3 studies/cv_vs_dv.py

export/CVCKAstudy.pdf:
	python3 studies/cvcka.py

cv_plots:
	python3 studies/cvqkd.py

export/EE.pdf:
	python3 studies/energy_efficiency.py

export/MeasuredValues.pdf:
	python3 studies/measured_values.py

export/piecharts.pdf:
	python3 studies/piecharts.py

export/DVprotocolstudy.pdf:
	python3 studies/qkd_protocols.py

export/timebinstudy.pdf:
	python3 studies/timevspolar.py

clean:
	rm -rf exports