#!/bin/bash
cd DEST_REPO
git pull origin main --rebase
git push origin HEAD 2>&1
